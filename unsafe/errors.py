"""Errors raised by the typed, non-offensive helpers."""


class ReadError(ValueError):
    """A file exists, but its metadata could not be read or written."""
