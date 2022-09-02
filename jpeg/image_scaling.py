import math
import time
import numpy as np
import skimage.transform
from skimage import color, img_as_float
from skimage.io import imread
from jpeg.image_util import *

from PIL import Image


def rescale_image_util(image, scale=4):
    height, width = image.shape

    out_image = np.zeros((height // scale, width // scale))

    for i in range(height // scale):
        for j in range(width // scale):
            out_image[i, j] = sum(image[i * scale:i * scale + scale, j * scale: j * scale + scale]) // math.pow(scale,
                                                                                                                2)

    return out_image


def rescale_image(image, scale=4):
    image_rescaled = rescale_image_util(image, scale)
    image_resized = resize_image(image_rescaled)
    return image_resized


def upscale(image, scale=4):
    height, width = image.shape
    out_image = np.zeros((height * scale, width * scale))

    for i in range(height):
        for j in range(width):
            out_image[i * scale:i * scale + scale, j * scale:j * scale + scale] = image[i, j]

    return out_image


# image = Image.open("../Examples/miner.jpg").convert('YCbCr')
# ycrcb_image = np.array(image)
#
# print(ycrcb_image.shape)
#
# print(np.min(ycrcb_image[:, :, 0]))
# print(np.max(ycrcb_image[:, :, 0]))
# print(np.min(ycrcb_image[:, :, 1]))
# print(np.max(ycrcb_image[:, :, 1]))
# print(np.min(ycrcb_image[:, :, 2]))
# print(np.max(ycrcb_image[:, :, 2]))
# print("-------")
#
# y = ycrcb_image[:, :, 0]
# cr = ycrcb_image[:, :, 1]
# cb = ycrcb_image[:, :, 2]

# image = (color.ycbcr2rgb(ycrcb_image) * 255).astype(np.uint8)
#
# image = color.ycbcr2rgb(image)
# print(image.max())
# print(image.min())
# imsave("../temp/ycbcr2rgb_without.jpg", image)
#
# print(np.min(image))
# print(np.max(image))
