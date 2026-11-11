import itertools
import os
import time
from typing import Dict, Optional

from PyPDF2 import PdfReader, PdfWriter

_output_ids = itertools.count()


def get_pdf_metadata(filename: str) -> Optional[Dict[str, str]]:
    """Extracts metadata from a PDF file.

    Args:
        filename (str): Path to the PDF file.

    Returns:
        A plain dictionary of PDF info, ``{}`` when none is present, or None on error.
    """
    try:
        with open(filename, 'rb') as file:
            pdf = PdfReader(file)
            metadata = pdf.metadata
        if not metadata:
            return {}
        return {
            str(key): "" if value is None else str(value)
            for key, value in metadata.items()
        }
    except Exception:
        return None


def del_pdf_metadata(filename: str) -> Optional[str]:
    """Removes metadata from a PDF and saves the output to a new file.

    Args:
        filename (str): Path to the PDF file.

    Returns:
        Optional[str]: Path to the output PDF file or None if an error occurs.
    """
    return _process_pdf(filename, new_metadata={})


def edit_pdf_metadata(filename: str, metadata: Dict[str, str]) -> Optional[str]:
    """Edits the metadata of a PDF file and saves the output to a new file.

    Args:
        filename (str): Path to the PDF file.
        metadata (Dict[str, str]): Metadata to update.

    Returns:
        Optional[str]: Path to the output PDF file or None if an error occurs.
    """
    formatted_metadata = {_metadata_key(key): value for key, value in metadata.items()}
    return _process_pdf(filename, new_metadata=formatted_metadata)


def _metadata_key(key: str) -> str:
    """Return a PDF name key, adding the leading slash when it is missing."""
    text = str(key).strip()
    if not text.startswith("/"):
        text = f"/{text}"
    return text


def _process_pdf(filename: str, new_metadata: Dict[str, str]) -> Optional[str]:
    """Processes a PDF file by either removing or updating its metadata.

    Args:
        filename (str): Path to the PDF file.
        new_metadata (Dict[str, str]): New metadata to apply to the PDF.

    Returns:
        Optional[str]: Path to the output PDF file or None if an error occurs.
    """
    try:
        with open(filename, 'rb') as file:
            pdf = PdfReader(file)
            output_pdf = PdfWriter()

            # Add all pages to the output PDF
            for page in pdf.pages:
                output_pdf.add_page(page)

            # Apply new metadata
            output_pdf.add_metadata(new_metadata)

            # Generate output folder and file paths
            output_folder = os.path.join(os.path.dirname(filename), 'output_PDF')
            os.makedirs(output_folder, exist_ok=True)
            timestamp = str(int(time.time() * 1000))
            output_file_path = os.path.join(
                output_folder, f'output_{timestamp}_{next(_output_ids)}.pdf'
            )

            # Save the new PDF
            with open(output_file_path, 'wb') as output_file:
                output_pdf.write(output_file)

            return output_file_path
    except FileNotFoundError:
        raise
    except Exception:
        return None
