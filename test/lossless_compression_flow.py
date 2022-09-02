import numpy as np
from skimage import color, morphology, filters

from encoding.huffman import *
from encoding.rle import find_eob, run_length_encoder
from jpeg.dct import *
from jpeg.image_util import *
from jpeg.zigzag import *
# from jpeg.compression import *
from jpeg.dictionary_util import *
# from jpeg.decompression import *
from jpeg.image_scaling import *
from jpeg.lossless_compression import *

import sys

import time

sys.setrecursionlimit(3000)

image = imread("../Examples/miner.jpg")
image = (color.rgb2gray(image) * 255).astype(np.uint8)

print(image.shape)
print(image[:8, :8])

start = time.time()
compressed = image_compression(image, True)
end = time.time()
print(end - start)


start = time.time()
image = decompress(compressed, False)
end = time.time()
print(end - start)

image = color.gray2rgb(image).astype(np.uint8)

print(np.min(image))
print(np.max(image))

imsave("decompressed_Y1.jpg", image)
print("decompression done!")
