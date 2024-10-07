import os
from typing import Dict

from .exif import Image


def get_image_metadata(path: str) -> Dict[str, str]:
    """Extracts EXIF metadata from an **JPG** image file if available.

    Args:
        path (str): The file path to the JPG image.

    Returns:
        Dict[str, str]: A dictionary containing the image's EXIF metadata, or an empty dictionary if no EXIF data is found.

    Raises:
        ValueError: If the provided path is not a valid file.
    """
    if not os.path.isfile(path):
        raise ValueError(f"Provided path '{path}' is not a valid file.")

    try:
        with open(path, 'rb') as image_file:
            image = Image(image_file)
    except Exception as e:
        raise ValueError(f"Failed to open or process image file: {e}")

    if not image.has_exif:
        return {}

    exif_dict = {}
    for tag in image.list_all():
        try:
            exif_dict[tag] = str(image.get(tag))
        except KeyError:
            continue  # Skip missing or unreadable EXIF tags

    return exif_dict


def del_image_metadata(path: str) -> bool:
    """Removes all EXIF metadata from an image file.

    Args:
        path (str): The file path to the image.

    Returns:
        bool: True if EXIF data was successfully removed, False if an error occurred.

    Raises:
        ValueError: If the provided path is not a valid file.
    """
    if not os.path.isfile(path):
        raise ValueError(f"Provided path '{path}' is not a valid file.")

    try:
        with open(path, 'rb') as image_file:
            image = Image(image_file)

        if image.has_exif:
            image.delete_all()

            with open(path, 'wb') as new_image_file:
                new_image_file.write(image.get_file())

        return True

    except Exception as e:
        return False


def edit_image_metadata(path: str, key: str, value: str) -> bool:
    """Edits or adds EXIF metadata to an image file.

    Args:
        path (str): The file path to the image.
        key (str): The EXIF tag to edit or add.
        value (str): The new value for the EXIF tag.

    Returns:
        bool: True if the EXIF metadata was successfully edited, False if an error occurred.

    Raises:
        ValueError: If the provided path is not a valid file or image.
    """
    if not os.path.isfile(path):
        raise ValueError(f"Provided path '{path}' is not a valid file.")

    try:
        with open(path, 'rb') as image_file:
            image = Image(image_file)

        # Modify or add the EXIF tag
        image[key] = value

        # Save the modified image back to the file
        with open(path, 'wb') as new_image_file:
            new_image_file.write(image.get_file())

        return True

    except Exception as e:
        return False
