import numpy as np
import skimage.transform
from PIL import ImageTk, Image
from pylab import *
from scipy import fftpack

from jpeg.image_util import resize_image

QUANTIZATION_MATRIX_4 = np.array([[16, 10, 24, 51],
                                  [14, 16, 40, 69],
                                  [18, 37, 68, 103],
                                  [49, 78, 103, 120]
                                  ])

QUANTIZATION_MATRIX = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                [12, 12, 14, 19, 26, 58, 60, 55],
                                [14, 13, 16, 24, 40, 57, 69, 56],
                                [14, 17, 22, 29, 51, 87, 80, 62],
                                [18, 22, 37, 56, 68, 109, 103, 77],
                                [24, 35, 55, 64, 81, 104, 113, 92],
                                [49, 64, 78, 87, 103, 121, 120, 101],
                                [72, 92, 95, 98, 112, 100, 103, 99]])

QUANTIZATION_MATRIX_16 = np.array([[16, 14, 11, 10, 10, 13, 16, 20, 24, 32, 40, 46, 51, 56, 61, 61],
                                   [14, 13, 12, 12, 12, 15, 18, 21, 25, 37, 49, 52, 56, 57, 58, 58],
                                   [12, 12, 12, 13, 14, 16, 19, 22, 26, 42, 58, 59, 60, 58, 55, 55],
                                   [13, 13, 12, 14, 15, 18, 22, 27, 33, 45, 58, 61, 64, 60, 56, 56],
                                   [14, 14, 13, 14, 16, 20, 24, 32, 40, 48, 57, 63, 69, 62, 56, 56],
                                   [14, 14, 15, 17, 19, 23, 26, 36, 46, 59, 72, 73, 74, 67, 59, 59],
                                   [14, 16, 17, 20, 22, 26, 29, 40, 51, 69, 87, 84, 80, 71, 62, 62],
                                   [16, 18, 20, 24, 30, 36, 42, 51, 60, 79, 98, 95, 92, 80, 70, 70],
                                   [18, 20, 22, 30, 37, 46, 56, 62, 68, 88, 109, 106, 103, 90, 77, 77],
                                   [21, 25, 28, 37, 46, 53, 60, 67, 74, 90, 106, 107, 108, 96, 84, 84],
                                   [24, 30, 35, 45, 55, 60, 64, 72, 81, 92, 104, 108, 113, 102, 92, 92],
                                   [36, 43, 50, 58, 66, 71, 76, 84, 92, 102, 112, 114, 116, 106, 96, 96],
                                   [49, 56, 64, 71, 78, 82, 87, 95, 103, 112, 121, 120, 120, 110, 101, 101],
                                   [60, 69, 78, 82, 86, 90, 92, 100, 108, 109, 110, 111, 112, 106, 100, 100],
                                   [72, 82, 92, 94, 95, 96, 98, 105, 112, 106, 100, 102, 103, 101, 99, 99],
                                   [72, 82, 92, 94, 95, 96, 98, 105, 112, 106, 100, 102, 103, 101, 99, 99]])


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

    sqr_h = image.shape[0] // block_size
    sqr_w = image.shape[1] // block_size

    out_image = np.zeros((image.shape[0], image.shape[1]))

    for i in range(sqr_h):
        for j in range(sqr_w):
            curr = image[i * block_size:i * block_size + block_size, j * block_size:j * block_size + block_size]
            dct_sp = fftpack.dct(fftpack.dct(curr.T, norm='ortho').T, norm='ortho').astype(int)

            out_image[i * block_size:i * block_size + block_size, j * block_size:j * block_size + block_size] = dct_sp

    return out_image.astype(int)


image = Image.open("../Examples/miner.jpg").convert('YCbCr')
image = np.array(image)
image = image[:, :, 0].astype(int)
image -= 128

print(image[:8, :8])

curr = image[:8, :8]
dct_sp = fftpack.dct(fftpack.dct(curr.T, norm='ortho').T, norm='ortho').astype(int)
print(dct_sp)
dct_sp = np.divide(dct_sp, QUANTIZATION_MATRIX).astype(int)
print(dct_sp)

print('-------------------')
print(image[25 * 8:25 * 8 + 8, :8])
curr = image[25 * 8:25 * 8 + 8, :8]
dct_sp = fftpack.dct(fftpack.dct(curr.T, norm='ortho').T, norm='ortho').astype(int)
print(dct_sp)
dct_sp = np.divide(dct_sp, QUANTIZATION_MATRIX).astype(int)
print(dct_sp)

dct_img = dct_image(image)

print('-------------------')
print(dct_img[0])
print()
print()
print()
print()

calc_dct_img = calc_dct(image)
print(calc_dct_img[:8, :8])
