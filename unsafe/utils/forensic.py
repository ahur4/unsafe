import mutagen
from PyPDF2 import PdfReader, PdfWriter
import os
from exif import Image
from typing import Optional, Union
import time


class Forensic:
    def __init__(self) -> None:
        ...

    # IMAGE #############################
    def extract_exif_img(self, path: str):
        if not os.path.isfile(path):
            raise ValueError("Your entered path not exists or not image.")
        with open(path, 'rb') as image_file:
            image = Image(image_file)
        if image.has_exif == True:
            exif_list = image.list_all()
            exif_dict = {}
            for i in exif_list:
                try:
                    exif_dict[f"{i}"] = f"{image[i]}"
                except:
                    ...
            return exif_dict
        else:
            return {}

    def delete_exif_img(self, path: str):
        if not os.path.isfile(path):
            raise ValueError("Your entered path not exists or not image.")
        try:
            with open(path, 'rb') as image_file:
                image = Image(image_file)

            image.delete_all()

            with open(path, 'wb') as new_image_file:
                new_image_file.write(image.get_file())
            return True
        except:
            return False

    def edit_exif_img(self, path: str, key: str, value: str):
        if not os.path.isfile(path):
            raise ValueError("Your entered path not exists or not image.")
        with open(path, 'rb') as image_file:
            image = image_file.read()
        try:
            image = Image(image)
            image[f"{key}"] = value
            with open(path, 'wb') as new:
                new.write(image.get_file())
            return True
        except Exception as e:
            return False

    # PDF ##############################
    def get_pdf_metadata(filename: str) -> dict:
        try:
            # Open the PDF file in read-only mode
            with open(filename, 'rb') as file:
                # Create a PDF object
                pdf = PdfReader(file)

                # Get the document info
                info = pdf.metadata

                # Return the metadata
                return info
        except Exception as e:
            print(e)
            return {}

    def remove_pdf_metadata(filename: str) -> Union[str, None]:
        # Open the PDF file in read-binary mode
        try:
            with open(filename, 'rb') as file:
                # Create a PDF object
                pdf = PdfReader(file)

                # Create a PDF object for the output file
                output_pdf = PdfWriter()

                # Add each page of the input PDF to the output PDF
                for page in range(len(pdf.pages)):
                    output_pdf.add_page(pdf.pages[page])

                # Remove the metadata from the output PDF
                output_pdf.add_metadata({})

                # Create the output folder if it doesn't exist
                output_folder_path = os.path.join(
                    os.path.dirname(filename), 'output PDF')
                if not os.path.exists(output_folder_path):
                    os.makedirs(output_folder_path)

                # Create the output file name with a timestamp
                timestamp = str(time.time()).replace('.', '')
                output_file_name = f'output_{timestamp}.pdf'

                # Create the output file path
                output_pdf_path = os.path.join(
                    output_folder_path, output_file_name)

                # Save the output PDF to the output file
                with open(output_pdf_path, 'wb') as output_file:
                    output_pdf.write(output_file)

            # Return the file path of the output PDF
            return output_pdf_path

        except FileNotFoundError:
            # If the input file is not found, return None
            return None

    def edit_pdf_metadata(filename: str, metadata: dict) -> Union[str, None]:
        # Open the PDF file in read-binary mode
        try:
            with open(filename, 'rb') as file:
                new_metadata = {}
                for j, k in metadata.items():
                    new_metadata[f"/{j}"] = k

                # Create a PDF object
                pdf = PdfReader(file)

                # Create a PDF object for the output file
                output_pdf = PdfWriter()

                # Add each page of the input PDF to the output PDF
                for page in range(len(pdf.pages)):
                    output_pdf.add_page(pdf.pages[page])

                # Update the metadata of the output PDF
                output_pdf.add_metadata(new_metadata)

                # Create the output folder if it doesn't exist
                output_folder_path = os.path.join(
                    os.path.dirname(filename), 'output PDF')
                if not os.path.exists(output_folder_path):
                    os.makedirs(output_folder_path)

                # Create the output file name with a timestamp
                timestamp = str(time.time()).replace('.', '')
                output_file_name = f'output_{timestamp}.pdf'

                # Create the output file path
                output_pdf_path = os.path.join(
                    output_folder_path, output_file_name)

                # Save the output PDF to the output file
                with open(output_pdf_path, 'wb') as output_file:
                    output_pdf.write(output_file)

            # Return the file path of the output PDF
            return output_pdf_path

        except FileNotFoundError:
            # If the input file is not found, return None
            return None

    # AUDIO ############################
    def get_audio_metadata(self, filename: str) -> dict:
        try:
            # Open the audio file using mutagen
            audio_file = mutagen.File(filename, easy=False)
            # Extract the EXIF data from the file
            exif_dict = {key: str(value) for key, value in audio_file.items()}
            # Return the EXIF data dictionary
            return exif_dict
        except Exception as e:
            print(e)
            # Return an empty dictionary if an error occurs
            return {}

    def remove_audio_metadata(self, filename: str) -> str:
        try:
            # Open the audio file using mutagen
            audio_file = mutagen.File(filename, easy=True)

            # Remove all EXIF data from the file
            audio_file.delete()

            # Create the output folder if it doesn't exist
            output_folder = "AUDIO_output"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Generate the output filename
            output_filename = f"output_{time.time()}.mp3"
            output_file_path = os.path.join(output_folder, output_filename)

            # Save the output file
            audio_file.save(output_file_path)

            # Return the full path of the output file
            return output_file_path
        except Exception as e:
            # Print an error message if an exception occurs
            print("An error occurred while deleting the EXIF data:", e)

            # Return an empty string if an error occurs
            return ""

    def edit_audio_metadata(self, filename: str, metadata: dict) -> str:
        try:
            # Open the audio file using mutagen
            audio_file = mutagen.File(filename, easy=True)

            # Edit the EXIF data for the file
            for key, value in metadata.items():
                audio_file[key] = value

            # Create the output folder if it doesn't exist
            output_folder = "AUDIO_output"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Generate the output filename
            output_filename = f"output_{time.time()}.mp3"
            output_file_path = os.path.join(output_folder, output_filename)

            # Save the output file
            audio_file.save(output_file_path)

            # Return the full path of the output file
            return output_file_path
        except Exception as e:
            # Print an error message if an exception occurs
            print("An error occurred while editing the EXIF data:", e)

            # Return an empty string if an error occurs
            return ""
