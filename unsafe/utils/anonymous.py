import cv2
from pathlib import Path
import os
import random
import string


class Anonymous:
    def __init__(self):
        ...

    def _string_generator(self, size=7, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def anon_picture(self, image_path: Path, casc_path: Path = 'unsafe/utils/datasets/front_sideview_face_detect.xml'):
        """
        Detect And Cover Faces for Anonymously.
        """
        if not os.path.exists('./anon_picture_cache'):
            os.mkdir('./anon_picture_cache')
        face_cascade = cv2.CascadeClassifier(casc_path)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 0), -1)
        file_path = f'anon_picture_cache/{self._string_generator()}.jpg'
        cv2.imwrite(file_path, image)
        return file_path

# a = Anonymous()
# print(a.anon_picture('unsafe/utils/testt.jpg'))
