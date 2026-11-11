"""Pydantic models for non-offensive results.

Attack, scanner, and brute-force modules do not use these types.
"""

from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class MetadataDocument(BaseModel):
    """String metadata for one file.

    ``entries`` is the whole payload. Item access reads that mapping, so
    ``document["title"]`` is the same as ``document.entries["title"]``.
    """

    model_config = ConfigDict(frozen=True)

    path: str
    entries: Dict[str, str] = Field(default_factory=dict)

    def __getitem__(self, key: str) -> str:
        return self.entries[key]

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and key in self.entries

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self.entries.get(key, default)


class PdfMetadata(MetadataDocument):
    """PDF info dictionary. Keys keep their leading slash, such as ``/Title``."""


class AudioMetadata(MetadataDocument):
    """Audio tags. ID3 files use names such as ``title`` and ``artist``."""


class ImageMetadata(MetadataDocument):
    """EXIF tags. ``entries`` is empty when the image has no EXIF block."""


class WrittenFile(BaseModel):
    """A file that was written successfully. Failure is an exception, not a missing path."""

    model_config = ConfigDict(frozen=True)

    path: str


class MacVendor(BaseModel):
    """Vendor for a MAC prefix from the local table.

    ``vendor`` is ``None`` when the prefix is well formed and not in the table.
    """

    model_config = ConfigDict(frozen=True)

    address: str
    prefix: str
    vendor: Optional[str] = None
