"""Pentesting helpers and shared client configuration.

Importing this package loads the existing feature modules. It does not silence
warnings for the rest of the process.
"""

from . import config, http
from .__version__ import __version__
from .errors import ReadError
from .ext import bruteforce, cryptography, exploits, forensic, network, web
from .models import AudioMetadata, ImageMetadata, MacVendor, PdfMetadata, WrittenFile

__all__ = [
    "__version__",
    "AudioMetadata",
    "ImageMetadata",
    "MacVendor",
    "PdfMetadata",
    "ReadError",
    "WrittenFile",
    "config",
    "http",
    "bruteforce",
    "cryptography",
    "exploits",
    "forensic",
    "network",
    "web",
]

__author__ = "Ahur4"
