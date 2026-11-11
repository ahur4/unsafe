"""Read and edit audio-file metadata.

Edits are written to a copy next to the source file. The copy keeps the
source extension. The original file is left unchanged.

Success returns a pydantic model. A missing file raises ``FileNotFoundError``.
A file that is not a recognized audio container raises ``ReadError``.
"""

from __future__ import annotations

import itertools
import os
import shutil
import time
from typing import Any, Dict, Mapping, Optional

from mutagen import File
from mutagen.id3 import ID3
from pydantic import TypeAdapter

from unsafe.errors import ReadError
from unsafe.models import AudioMetadata, WrittenFile

_output_ids = itertools.count()
_STRING_MAP = TypeAdapter(Dict[str, str])


def get_audio_metadata(filename: str) -> AudioMetadata:
    """Return tags from an audio file.

    ID3 tags use common names such as ``title`` and ``artist`` when mutagen
    knows that name. An audio file with no tags has empty ``entries``.
    """
    audio = _open_audio(filename)
    try:
        return AudioMetadata(path=filename, entries=_read_tags(audio))
    except ReadError:
        raise
    except Exception as exc:
        raise ReadError(f"Could not read audio metadata from {filename}") from exc


def del_audio_metadata(filename: str) -> WrittenFile:
    """Copy an audio file without its tags."""
    return _process_audio(filename, new_metadata=None)


def edit_audio_metadata(filename: str, metadata: Mapping[str, str]) -> WrittenFile:
    """Copy an audio file and set string metadata on the copy.

    ID3 files accept the usual easy names (``title``, ``artist``, ``album``,
    and so on). An unknown name raises ``ValueError``.
    """
    checked = _STRING_MAP.validate_python(dict(metadata))
    return _process_audio(filename, new_metadata=checked)


def _open_audio(filename: str) -> Any:
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)
    try:
        audio = File(filename, easy=True)
    except Exception as exc:
        raise ReadError(f"Could not open audio file {filename}") from exc
    if audio is None:
        raise ReadError(f"Unrecognized audio file: {filename}")
    return audio


def _process_audio(filename: str, new_metadata: Optional[Dict[str, str]]) -> WrittenFile:
    """Copy ``filename`` and either clear or replace its tags."""
    _open_audio(filename)
    output_path = _output_path(filename)
    try:
        shutil.copy2(filename, output_path)
        audio = File(output_path, easy=True)
        if audio is None:
            raise ReadError(f"Unrecognized audio file: {filename}")
        if new_metadata is None:
            audio.delete()
        else:
            _apply_tags(audio, new_metadata)
        audio.save()
        return WrittenFile(path=output_path)
    except Exception as exc:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except OSError:
                pass
        if isinstance(exc, (ReadError, ValueError)):
            raise
        raise ReadError(f"Could not write audio metadata for {filename}") from exc


def _output_path(filename: str) -> str:
    directory = os.path.dirname(os.path.abspath(filename))
    output_folder = os.path.join(directory, "AUDIO_output")
    os.makedirs(output_folder, exist_ok=True)
    timestamp = str(int(time.time() * 1000))
    suffix = os.path.splitext(filename)[1] or ".bin"
    return os.path.join(output_folder, f"output_{timestamp}_{next(_output_ids)}{suffix}")


def _read_tags(audio: Any) -> Dict[str, str]:
    tags = getattr(audio, "tags", None)
    if isinstance(tags, ID3):
        return _easy_id3_values(tags)
    values: Dict[str, str] = {}
    for key, value in audio.items():
        values[str(key)] = _stringify(value)
    return values


def _easy_id3_values(tags: ID3) -> Dict[str, str]:
    from mutagen.easyid3 import EasyID3

    found: Dict[str, str] = {}
    getters = getattr(EasyID3, "Get", {})
    for key, getter in getters.items():
        if "*" in key:
            continue
        try:
            found[key] = _stringify(getter(tags, key))
        except KeyError:
            continue
    return found


def _apply_tags(audio: Any, metadata: Mapping[str, Optional[str]]) -> None:
    """Assign string tags, falling back to ID3 easy names when required."""
    try:
        for key, value in metadata.items():
            audio[key] = "" if value is None else str(value)
        return
    except TypeError:
        pass

    from mutagen.easyid3 import EasyID3

    if getattr(audio, "tags", None) is None:
        audio.add_tags()
    tags = audio.tags
    if not isinstance(tags, ID3):
        raise ValueError("string metadata is not supported for this audio format")
    setters = getattr(EasyID3, "Set", {})
    for key, value in metadata.items():
        normalized = str(key).lower()
        setter = setters.get(normalized)
        if setter is None:
            raise ValueError(f"unsupported metadata key: {key}")
        text = "" if value is None else str(value)
        setter(tags, normalized, [text])


def _stringify(value: object) -> str:
    if isinstance(value, (list, tuple)):
        return ", ".join(_stringify(item) for item in value)
    text = getattr(value, "text", None)
    if isinstance(text, (list, tuple)):
        return ", ".join(str(item) for item in text)
    if text is not None:
        return str(text)
    return str(value)
