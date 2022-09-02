import numpy as np
from skimage import color

from encoding.huffman import *
from encoding.rle import find_eob, run_length_encoder
from jpeg.dct import *
from jpeg.image_util import *
from jpeg.zigzag import *
from jpeg.compression import *
from jpeg.dictionary_util import *

from PIL import Image

image = Image.open("../Examples/miner.jpg").convert('YCbCr')
image = np.array(image)
image = image[:, :, 0].astype(int)
print(image.shape)
print(image[80:88, 200:208])

# image_y = imread("../test/Y_after_compression.jpg")
# image_y = (color.rgb2gray(image_y) * 255).astype(np.uint8)
#
# print(image_y[80:88, 200:208])


arr = image[80:88, 200:208]
arr = arr - 128
print(arr[:, :])

dct_sp = fftpack.dct(fftpack.dct(arr.T, norm='ortho', type=2).T, norm='ortho', type=2)
print(dct_sp[:, :])

quatized = np.divide(dct_sp, QUANTIZATION_MATRIX).astype(int)

print("division")
print(quatized[:, :])

tek = quatized * QUANTIZATION_MATRIX
print(tek[:, :])
tek = fftpack.idct(fftpack.idct(tek.T, norm='ortho', type=2).T, norm='ortho', type=2)
tek = tek + 128
tek = tek.astype(np.uint8)

print(tek[:, :])
###############
start = time.time()

resized = np.zeros((10, 10))
resized[1:-1, 1:-1] = tek
# print(resized)
resized[0, :] = resized[2, :]
resized[9, :] = resized[7, :]
resized[:, 0] = resized[:, 2]
resized[:, 9] = resized[:, 7]
# print(resized)

i, j = np.where(resized[1:-1, 1:-1] > 250)
i += 1
j += 1
# print(i)
# print(j)

print(resized[1:-1, 1:-1])
for k in range(len(i)):
    resized[i[k], j[k]] = np.median(resized[i[k] - 1:i[k] + 2, j[k] - 1: j[k] + 2])

end = time.time()
print(end - start)

print(resized[1:-1, 1:-1])
