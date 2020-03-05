import math
import cv2 as cv
import numpy as np

from .flask_config import fg_path, a_path, bg_path
from .flask_utils import merge_image_name


def process(im_name, bg_name):
    name = merge_image_name(im_name, bg_name)
    im = cv.imread(fg_path + im_name)
    a = cv.imread(a_path + im_name, 0)
    h, w = im.shape[:2]
    bg = cv.imread(bg_path + bg_name)
    bh, bw = bg.shape[:2]
    wratio = w / bw
    hratio = h / bh
    ratio = wratio if wratio > hratio else hratio
    if ratio > 1:
        bg = cv.resize(src=bg, dsize=(math.ceil(bw * ratio), math.ceil(bh * ratio)), interpolation=cv.INTER_CUBIC)

    return composite4(im, bg, a, w, h, name)


def composite4(fg, bg, a, w, h, name):
    fg = np.array(fg, np.float32)
    cv.imwrite('./static/merge/{}-fg.png'.format(name), fg)
    bg_h, bg_w = bg.shape[:2]
    x = max(0, int((bg_w - w) / 2))
    y = max(0, int((bg_h - h) / 2))
    crop = np.array(bg[y:y + h, x:x + w], np.float32)
    cv.imwrite('./static/merge/{}-bg.png'.format(name), bg)

    alpha = np.zeros((h, w, 1), np.float32)
    alpha[:, :, 0] = a / 255.

    im = alpha * fg + (1 - alpha) * crop
    im = im.astype(np.uint8)
    cv.imwrite('./static/merge/{}-merge.png'.format(name), im)

    new_a = np.zeros((bg_h, bg_w), np.uint8)
    new_a[y:y + h, x:x + w] = a
    new_im = bg.copy()
    new_im[y:y + h, x:x + w] = im
    return new_im, new_a, fg, bg