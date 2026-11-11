"""File-metadata helpers. Sample bytes stay inside the temp directory."""

import shutil
import struct
import wave
from pathlib import Path

import pytest
from pypdf import PdfWriter

from unsafe.errors import ReadError
from unsafe.ext.forensic.audio import (
    del_audio_metadata,
    edit_audio_metadata,
    get_audio_metadata,
)
from unsafe.ext.forensic.images import (
    del_image_metadata,
    edit_image_metadata,
    get_image_metadata,
)
from unsafe.ext.forensic.pdf import (
    del_pdf_metadata,
    edit_pdf_metadata,
    get_pdf_metadata,
)

SAMPLE_IMAGE = (
    Path(__file__).resolve().parents[1] / "example" / "forensic" / "images" / "DSCN0029.jpg"
)


def _wav(path: Path) -> None:
    with wave.open(str(path), "w") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(8000)
        handle.writeframes(struct.pack("<h", 0) * 80)


def _pdf(path: Path, title: str = "Hello") -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.add_metadata({"/Title": title})
    with path.open("wb") as handle:
        writer.write(handle)


def test_pdf_round_trip(tmp_path):
    source = tmp_path / "a.pdf"
    _pdf(source)
    metadata = get_pdf_metadata(str(source))
    assert metadata["/Title"] == "Hello"
    assert metadata.model_dump()["entries"]["/Title"] == "Hello"

    edited = edit_pdf_metadata(str(source), {"Author": "Ada", "/Subject": "Notes"})
    updated = get_pdf_metadata(edited.path)
    assert updated["/Author"] == "Ada"
    assert updated["/Subject"] == "Notes"
    assert "/Title" not in updated

    cleared = del_pdf_metadata(str(source))
    assert "/Title" not in get_pdf_metadata(cleared.path)
    with pytest.raises(FileNotFoundError):
        get_pdf_metadata(str(tmp_path / "missing.pdf"))
    with pytest.raises(FileNotFoundError):
        del_pdf_metadata(str(tmp_path / "missing.pdf"))

    garbage = tmp_path / "bad.pdf"
    garbage.write_bytes(b"not a pdf")
    with pytest.raises(ReadError):
        get_pdf_metadata(str(garbage))
    with pytest.raises(ReadError):
        edit_pdf_metadata(str(garbage), {"Author": "A"})


def test_audio_edit_writes_a_real_copy(tmp_path):
    source = tmp_path / "clip.wav"
    _wav(source)
    assert get_audio_metadata(str(source)).entries == {}

    edited = edit_audio_metadata(str(source), {"title": "Hello", "artist": "Ada"})
    assert edited.path.endswith(".wav")
    assert Path(edited.path).parent == tmp_path / "AUDIO_output"
    tagged = get_audio_metadata(edited.path)
    assert tagged["title"] == "Hello"
    assert tagged["artist"] == "Ada"
    assert tagged.model_dump()["entries"]["title"] == "Hello"
    assert get_audio_metadata(str(source)).entries == {}
    with wave.open(edited.path) as handle:
        assert handle.getnframes() == 80

    cleared = del_audio_metadata(edited.path)
    assert "title" not in get_audio_metadata(cleared.path)

    again = edit_audio_metadata(str(source), {"title": "Second"})
    assert again.path != edited.path

    with pytest.raises(ValueError):
        edit_audio_metadata(str(source), {"not-a-real-tag": "x"})
    with pytest.raises(FileNotFoundError):
        get_audio_metadata(str(tmp_path / "missing.wav"))
    empty = tmp_path / "empty.bin"
    empty.write_bytes(b"")
    with pytest.raises(ReadError):
        get_audio_metadata(str(empty))
    with pytest.raises(ReadError):
        edit_audio_metadata(str(empty), {"title": "nope"})


def test_audio_string_tags_and_unsupported_formats():
    from unsafe.ext.forensic import audio as audio_mod

    class Easy:
        def __init__(self):
            self.tags = None
            self.stored = {}

        def items(self):
            return self.stored.items()

        def __setitem__(self, key, value):
            self.stored[key] = value

    easy = Easy()
    audio_mod._apply_tags(easy, {"title": None})
    assert easy.stored["title"] == ""
    assert audio_mod._read_tags(easy) == {"title": ""}

    class Text:
        text = "hi"

    class Words:
        text = ["a", "b"]

    assert audio_mod._stringify(Text()) == "hi"
    assert audio_mod._stringify(Words()) == "a, b"

    class RejectsStrings:
        def __init__(self):
            self.tags = None
            self.added = False

        def __setitem__(self, key, value):
            raise TypeError("needs frames")

        def add_tags(self):
            self.added = True
            self.tags = object()

    rejected = RejectsStrings()
    with pytest.raises(ValueError):
        audio_mod._apply_tags(rejected, {"title": "x"})
    assert rejected.added is True


def test_pdf_without_info_dictionary(tmp_path, monkeypatch):
    source = tmp_path / "empty-info.pdf"
    source.write_bytes(b"%PDF-1.4\n")

    class _Reader:
        def __init__(self, handle):
            self.metadata = None

    monkeypatch.setattr("unsafe.ext.forensic.pdf.PdfReader", _Reader)
    assert get_pdf_metadata(str(source)).entries == {}


def test_image_metadata_round_trip(tmp_path, monkeypatch):
    original = SAMPLE_IMAGE.read_bytes()
    metadata = get_image_metadata(str(SAMPLE_IMAGE))
    assert metadata["make"] == "NIKON"
    assert SAMPLE_IMAGE.read_bytes() == original

    copy = tmp_path / "photo.jpg"
    shutil.copyfile(SAMPLE_IMAGE, copy)
    written = edit_image_metadata(str(copy), "image_description", "Hello")
    assert written.path == str(copy)
    assert get_image_metadata(str(copy))["image_description"] == "Hello"
    assert del_image_metadata(str(copy)).path == str(copy)
    assert get_image_metadata(str(copy)).entries == {}
    with pytest.raises(FileNotFoundError):
        get_image_metadata(str(tmp_path / "missing.jpg"))
    with pytest.raises(FileNotFoundError):
        del_image_metadata(str(tmp_path / "missing.jpg"))
    with pytest.raises(FileNotFoundError):
        edit_image_metadata(str(tmp_path / "missing.jpg"), "image_description", "x")

    tiny = tmp_path / "tiny.jpg"
    tiny.write_bytes(b"\xff\xd8\xff\xd9")
    assert get_image_metadata(str(tiny)).entries == {}
    assert del_image_metadata(str(tiny)).path == str(tiny)

    def _boom(_handle):
        raise RuntimeError("unreadable")

    monkeypatch.setattr("unsafe.ext.forensic.images.Image", _boom)
    with pytest.raises(ReadError):
        get_image_metadata(str(tiny))
    with pytest.raises(ReadError):
        del_image_metadata(str(tiny))
    with pytest.raises(ReadError):
        edit_image_metadata(str(tiny), "image_description", "x")
