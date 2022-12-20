from unsafe.utils.encrypt import Encryptor
from unsafe.utils.decrypt import Decrypter
from unsafe.utils.proxy import Proxy
from unsafe.utils.bruteforce import BruteForcer
from unsafe.utils.wp import Wordpress
from unsafe.utils.exifdata import ExifImage
from unsafe.utils.anonymous import Anonymous
from unsafe.utils.seeker import Seeker

class Unsafe(
    Encryptor,
    Decrypter,
    Proxy,
    BruteForcer,
    Wordpress,
    ExifImage,
    Anonymous,
    Seeker
):
    ...
