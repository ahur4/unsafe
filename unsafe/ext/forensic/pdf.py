"""Read and edit PDF document info.

Success always returns a pydantic model. A missing file raises
``FileNotFoundError``. A file that cannot be parsed raises ``ReadError``.
"""

from __future__ import annotations

import itertools
import os
import time
from typing import Dict, Mapping

from pydantic import TypeAdapter
from pypdf import PdfReader, PdfWriter

from unsafe.errors import ReadError
from unsafe.models import PdfMetadata, WrittenFile

_output_ids = itertools.count()
_STRING_MAP = TypeAdapter(Dict[str, str])


def get_pdf_metadata(filename: str) -> PdfMetadata:
    """Return the PDF info dictionary.

    An info dictionary that is absent is an empty ``entries`` mapping, not
    ``None``.
    """
    _require_file(filename)
    try:
        with open(filename, "rb") as handle:
            pdf = PdfReader(handle)
            metadata = pdf.metadata
        entries: Dict[str, str] = {}
        if metadata:
            for key, value in metadata.items():
                entries[str(key)] = "" if value is None else str(value)
        return PdfMetadata(path=filename, entries=entries)
    except ReadError:
        raise
    except Exception as exc:
        raise ReadError(f"Could not read PDF metadata from {filename}") from exc


def del_pdf_metadata(filename: str) -> WrittenFile:
    """Write a copy of ``filename`` without the previous info keys."""
    return _process_pdf(filename, new_metadata={})


def edit_pdf_metadata(filename: str, metadata: Mapping[str, str]) -> WrittenFile:
    """Write a copy of ``filename`` whose info dictionary is ``metadata``.

    Keys may omit the leading slash. Values must be strings.
    """
    checked = _STRING_MAP.validate_python(dict(metadata))
    formatted = {_metadata_key(key): value for key, value in checked.items()}
    return _process_pdf(filename, new_metadata=formatted)


def _metadata_key(key: str) -> str:
    """Return a PDF name key, adding the leading slash when it is missing."""
    text = str(key).strip()
    if not text.startswith("/"):
        text = f"/{text}"
    return text


def _process_pdf(filename: str, new_metadata: Dict[str, str]) -> WrittenFile:
    """Copy ``filename`` and replace its document info."""
    _require_file(filename)
    try:
        with open(filename, "rb") as handle:
            pdf = PdfReader(handle)
            output_pdf = PdfWriter()
            for page in pdf.pages:
                output_pdf.add_page(page)
            output_pdf.add_metadata(new_metadata)
            output_folder = os.path.join(os.path.dirname(filename), "output_PDF")
            os.makedirs(output_folder, exist_ok=True)
            timestamp = str(int(time.time() * 1000))
            output_file_path = os.path.join(
                output_folder, f"output_{timestamp}_{next(_output_ids)}.pdf"
            )
            with open(output_file_path, "wb") as output_file:
                output_pdf.write(output_file)
        return WrittenFile(path=output_file_path)
    except ReadError:
        raise
    except Exception as exc:
        raise ReadError(f"Could not write PDF metadata for {filename}") from exc


def _require_file(filename: str) -> None:
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)
