from datetime import datetime

from PIL.Image import Exif
from PIL.ExifTags import  GPSTAGS
import pillow_heif
from PIL import Image
from PIL.ExifTags import TAGS

pillow_heif.register_heif_opener()

def get_exif(file_name) -> Exif:
    image: Image.Image = Image.open(file_name)
    return image.getexif()


def get_geo(exif):
    global tag_key
    for key, value in TAGS.items():
        if value == "GPSInfo":
            tag_key = key
    gps_info = exif.get_ifd(tag_key)
    return {
        GPSTAGS.get(key, key): value
        for key, value in gps_info.items()
    }



def extract_timestamp(image_path):
    image = Image.open(image_path)
    exif_data = image.getexif()

    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal' or tag_name == 'DateTime':
                if value:
                    # 转换时间格式为 YYYYMMDD_HHMMSS
                    value_corrected = value.replace(":", "-", 2)  # Replace only the first two colons
                    dt = datetime.fromisoformat(value_corrected)
                    return dt.strftime("%Y%m%d_%H%M%S")
                return None

    return None




