"""Read and modify image EXIF metadata using Python."""

from ._constants import (
    ColorSpace,
    ExposureMode,
    ExposureProgram,
    GpsAltitudeRef,
    LightSource,
    MeteringMode,
    Orientation,
    ResolutionUnit,
    Saturation,
    SceneCaptureType,
    SensingMethod,
    Sharpness,
    WhiteBalance,
)
from ._datatypes import Flash, FlashMode, FlashReturn
from ._image import Image

DATETIME_STR_FORMAT = "%Y:%m:%d %H:%M:%S"
