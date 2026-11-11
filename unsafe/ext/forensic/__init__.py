"""File metadata helpers and their pydantic result models."""

from .audio import del_audio_metadata, edit_audio_metadata, get_audio_metadata
from .images import del_image_metadata, edit_image_metadata, get_image_metadata
from .pdf import del_pdf_metadata, edit_pdf_metadata, get_pdf_metadata
from unsafe.models import AudioMetadata, ImageMetadata, PdfMetadata, WrittenFile

__all__ = [
    "AudioMetadata",
    "ImageMetadata",
    "PdfMetadata",
    "WrittenFile",
    "get_audio_metadata",
    "del_audio_metadata",
    "edit_audio_metadata",
    "get_image_metadata",
    "del_image_metadata",
    "edit_image_metadata",
    "get_pdf_metadata",
    "del_pdf_metadata",
    "edit_pdf_metadata",
]
__author__ = "Ahur4"
