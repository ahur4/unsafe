"""Read and edit audio-file metadata.

Edits are written to a copy next to the source file. The copy keeps the
source extension. The original file is left unchanged.
"""

import itertools
import os
import shutil
import time
from typing import Dict, Optional

from mutagen import File
from mutagen.id3 import ID3

_output_ids = itertools.count()


def get_audio_metadata(filename: str) -> Optional[Dict[str, str]]:
    """Extract metadata from an audio file.

    ID3 tags are returned under common names such as ``title`` and ``artist``
    when mutagen knows that name. Other formats use their native keys.

    Args:
        filename: Path to the audio file.

    Returns:
        A dictionary of metadata, or None if the file cannot be read.
        An empty dictionary means the file loaded and has no tags.
    """
    try:
        audio = File(filename, easy=True)
    except Exception:
        return None
    if audio is None:
        return None
    try:
        return _read_tags(audio)
    except Exception:
        return None


def del_audio_metadata(filename: str) -> Optional[str]:
    """Copy an audio file without its tags.

    Args:
        filename: Path to the audio file.

    Returns:
        Path to the copy, or None if the file cannot be processed.
    """
    return _process_audio(filename, new_metadata=None)


def edit_audio_metadata(filename: str, metadata: Dict[str, str]) -> Optional[str]:
    """Copy an audio file and set string metadata on the copy.

    Args:
        filename: Path to the audio file.
        metadata: Tag names and string values. ID3 files accept the usual
            easy names (``title``, ``artist``, ``album``, and so on).

    Returns:
        Path to the copy, or None if the file cannot be processed.
    """
    return _process_audio(filename, new_metadata=metadata)


def _process_audio(filename: str, new_metadata: Optional[Dict[str, str]]) -> Optional[str]:
    """Copy ``filename`` and either clear or replace its tags."""
    output_path = None
    try:
        if File(filename, easy=True) is None:
            return None
        output_path = _output_path(filename)
        shutil.copy2(filename, output_path)
        audio = File(output_path, easy=True)
        if audio is None:
            raise ValueError("unrecognized audio file")
        if new_metadata is None:
            audio.delete()
        else:
            _apply_tags(audio, new_metadata)
        audio.save()
        return output_path
    except Exception:
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except OSError:
                pass
        return None


def _output_path(filename: str) -> str:
    directory = os.path.dirname(os.path.abspath(filename))
    output_folder = os.path.join(directory, "AUDIO_output")
    os.makedirs(output_folder, exist_ok=True)
    timestamp = str(int(time.time() * 1000))
    suffix = os.path.splitext(filename)[1] or ".bin"
    return os.path.join(output_folder, f"output_{timestamp}_{next(_output_ids)}{suffix}")


def _read_tags(audio) -> Dict[str, str]:
    tags = getattr(audio, "tags", None)
    if isinstance(tags, ID3):
        return _easy_id3_values(tags)
    values = {}
    for key, value in audio.items():
        values[str(key)] = _stringify(value)
    return values


def _easy_id3_values(tags: ID3) -> Dict[str, str]:
    from mutagen.easyid3 import EasyID3

    found: Dict[str, str] = {}
    for key, getter in EasyID3.Get.items():
        if "*" in key:
            continue
        try:
            found[key] = _stringify(getter(tags, key))
        except KeyError:
            continue
    return found


def _apply_tags(audio, metadata: Dict[str, str]) -> None:
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
    for key, value in metadata.items():
        normalized = str(key).lower()
        setter = EasyID3.Set.get(normalized)
        if setter is None:
            raise ValueError(f"unsupported metadata key: {key}")
        text = "" if value is None else str(value)
        setter(tags, normalized, [text])


def _stringify(value) -> str:
    if isinstance(value, (list, tuple)):
        return ", ".join(_stringify(item) for item in value)
    text = getattr(value, "text", None)
    if isinstance(text, (list, tuple)):
        return ", ".join(str(item) for item in text)
    if text is not None:
        return str(text)
    return str(value)
