from skimage import color

from encoding.huffman import *
from encoding.rle import find_eob, run_length_encoder
from jpeg.dct import *
from jpeg.image_util import *
from jpeg.zigzag import *
from jpeg.compression import *
from jpeg.dictionary_util import *
from jpeg.decompression import *

import time

# # load image
#
# image = imread("../Examples/miner.jpg")
#
# image = (color.rgb2gray(image) * 255).astype(int)
#
# start = time.time()
# out = image_compression(image)
# end = time.time()
#
# print(end - start)
# load image

image = imread("../Examples/miner.jpg")

image = (color.rgb2gray(image) * 255).astype(np.uint8)

image = resize_image(image)

image = image_compression(image)
print(image)
print(len(image))
image = decompress(image, False)


image = color.gray2rgb(image).astype(np.uint8)

print(np.min(image))
print(np.max(image))

imsave("decompressed_Y1.jpg", image)
print("decompression done!")
