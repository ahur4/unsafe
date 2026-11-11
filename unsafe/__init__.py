"""Pentesting helpers and shared client configuration.

Importing this package loads the existing feature modules. It does not silence
warnings for the rest of the process.
"""

from .__version__ import __version__
from . import config, http
from .ext import bruteforce
from .ext import cryptography
from .ext import exploits
from .ext import forensic
from .ext import network
from .ext import web

__all__ = [
    "__version__",
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
