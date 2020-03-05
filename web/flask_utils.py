import datetime
import io
from PIL import Image


def tid_maker():
    return '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())


def merge_image_name(image1, image2):
    name1 = image1.split('.')[0]
    name2 = image2.split('.')[0]
    name = name1 + '-' + name2
    return name


def change_image_channels(image_content, save_path):
    image = Image.open(io.BytesIO(image_content))
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        image = Image.merge("RGB", (r, g, b))
    elif image.mode != 'RGB':
        image = image.convert("RGB")
    image.save(save_path)


def change_channels_to_rgb(image_path):
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
        image.save(image_path)


# image_content = image.read()
# change_image_channels(image.read(), in_path)
