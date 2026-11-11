"""Read and edit JPEG EXIF metadata.

Success returns a pydantic model. A missing path raises ``FileNotFoundError``.
A file that cannot be processed raises ``ReadError``.
"""

from __future__ import annotations

import os
from typing import Dict

from unsafe.errors import ReadError
from unsafe.models import ImageMetadata, WrittenFile

from .exif import Image


def get_image_metadata(path: str) -> ImageMetadata:
    """Return EXIF tags for a JPEG file.

    ``entries`` is empty when the file has no EXIF block.
    """
    _require_file(path)
    image = _open_image(path)
    if not image.has_exif:
        return ImageMetadata(path=path, entries={})
    entries: Dict[str, str] = {}
    for tag in image.list_all():
        try:
            entries[str(tag)] = str(image.get(tag))
        except KeyError:
            continue
    return ImageMetadata(path=path, entries=entries)


def del_image_metadata(path: str) -> WrittenFile:
    """Remove EXIF metadata from ``path`` itself."""
    _require_file(path)
    try:
        image = _open_image(path)
        if image.has_exif:
            image.delete_all()
            with open(path, "wb") as handle:
                handle.write(image.get_file())
    except ReadError:
        raise
    except Exception as exc:
        raise ReadError(f"Could not remove image metadata from {path}") from exc
    return WrittenFile(path=path)


def edit_image_metadata(path: str, key: str, value: str) -> WrittenFile:
    """Set one EXIF tag on ``path`` itself."""
    _require_file(path)
    if not isinstance(key, str) or not isinstance(value, str):
        raise TypeError("EXIF key and value must be strings")
    try:
        image = _open_image(path)
        image[key] = value
        with open(path, "wb") as handle:
            handle.write(image.get_file())
    except ReadError:
        raise
    except Exception as exc:
        raise ReadError(f"Could not edit image metadata in {path}") from exc
    return WrittenFile(path=path)


def _require_file(path: str) -> None:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)


def _open_image(path: str) -> Image:
    try:
        with open(path, "rb") as handle:
            return Image(handle)
    except ReadError:
        raise
    except Exception as exc:
        raise ReadError(f"Could not open image {path}") from exc
