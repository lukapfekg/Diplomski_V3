import numpy as np
from PIL import ImageTk, Image
from pylab import *
from scipy import fftpack

from jpeg.image_util import resize_image

QUANTIZATION_MATRIX = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                [12, 12, 14, 19, 26, 58, 60, 55],
                                [14, 13, 16, 24, 40, 57, 69, 56],
                                [14, 17, 22, 29, 51, 87, 80, 62],
                                [18, 22, 37, 56, 68, 109, 103, 77],
                                [24, 35, 55, 64, 81, 104, 113, 92],
                                [49, 64, 78, 87, 103, 121, 120, 101],
                                [72, 92, 95, 98, 112, 100, 103, 99]])


def dct_image(image, lossless=False):
    sqr_h = image.shape[0] // 8
    sqr_w = image.shape[1] // 8

    out_array = []

    for i in range(sqr_h):
        for j in range(sqr_w):
            curr = image[i * 8:i * 8 + 8, j * 8:j * 8 + 8]
            dct_sp = fftpack.dct(fftpack.dct(curr.T, norm='ortho').T, norm='ortho').astype(int)

            if not lossless:
                dct_sp = np.divide(dct_sp, QUANTIZATION_MATRIX).astype(int)

            out_array.append(dct_sp)

    return out_array


def calc_dct(image, block_size=8):
    image = resize_image(image, block_size).astype(np.uint8)

    sqr_h = image.shape[0] // 8
    sqr_w = image.shape[1] // 8

    out_image = np.zeros((image.shape[0], image.shape[1]))

    for i in range(sqr_h):
        for j in range(sqr_w):
            curr = image[i * 8:i * 8 + 8, j * 8:j * 8 + 8]
            dct_sp = fftpack.dct(fftpack.dct(curr.T, norm='ortho').T, norm='ortho').astype(int)

            # dct_sp = np.divide(dct_sp, QUANTIZATION_MATRIX).astype(int)

            out_image[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = dct_sp

    return out_image.astype(int)


# image = Image.open("../Examples/miner.jpg").convert('YCbCr')
# image = np.array(image)
# # image = imread("../Examples/miner.jpg")
# r = image[:, :, 0]
#
# r_dct = calc_dct(r, 16)
# r_dct_first = dct_image(r, False)
#
# print(r_dct[:16, :16])
# print(r_dct_first[0])
