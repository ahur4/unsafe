from PIL import Image
from pathlib import Path
import os
from exif import Image


class ExifImage:
    def __init__(self) -> None:
        ...

    def extract_exif_img(self, path: Path):
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

    def delete_exif_img(self, path: Path):
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

    def edit_exif_image(self, path: Path, key: str, value: str):
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
