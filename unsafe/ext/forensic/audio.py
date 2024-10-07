import os
import time
from typing import Dict, Optional

from mutagen import File


def get_audio_metadata(filename: str) -> Optional[Dict[str, str]]:
    """Extracts metadata from an audio file.

    Args:
        filename (str): Path to the audio file.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the audio metadata, or None if an error occurs.
    """
    try:
        audio_file = File(filename, easy=False)
        return {key: str(value) for key, value in audio_file.items()}
    except Exception as e:
        return None


def del_audio_metadata(filename: str) -> Optional[str]:
    """Removes metadata from an audio file and saves the result.

    Args:
        filename (str): Path to the audio file.

    Returns:
        Optional[str]: Path to the output file or None if an error occurs.
    """
    return _process_audio(filename, new_metadata=None)


def edit_audio_metadata(filename: str, metadata: Dict[str, str]) -> Optional[str]:
    """Edits the metadata of an audio file and saves the result.

    Args:
        filename (str): Path to the audio file.
        metadata (Dict[str, str]): Metadata to update.

    Returns:
        Optional[str]: Path to the output file or None if an error occurs.
    """
    return _process_audio(filename, new_metadata=metadata)


def _process_audio(filename: str, new_metadata: Optional[Dict[str, str]]) -> Optional[str]:
    """Processes an audio file by removing or updating its metadata.

    Args:
        filename (str): Path to the audio file.
        new_metadata (Optional[Dict[str, str]]): New metadata to apply, or None to remove metadata.

    Returns:
        Optional[str]: Path to the output file or None if an error occurs.
    """
    try:
        audio_file = File(filename, easy=True)

        # Remove or update metadata.
        if new_metadata is None:
            audio_file.delete()
        else:
            for key, value in new_metadata.items():
                audio_file[key] = value

        # Create the output folder if it doesnt exist.
        output_folder = "AUDIO_output"
        os.makedirs(output_folder, exist_ok=True)

        # Generate the output filename.
        timestamp = str(int(time.time() * 1000))
        output_filename = f"output_{timestamp}.mp3"
        output_file_path = os.path.join(output_folder, output_filename)

        # Save the new audio file.
        audio_file.save(output_file_path)

        return output_file_path
    except Exception as e:
        return None
