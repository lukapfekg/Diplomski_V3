import numpy as np
from skimage import color, morphology, filters

from encoding.huffman import *
from encoding.rle import find_eob, run_length_encoder
from jpeg.dct import *
from jpeg.image_util import *
from jpeg.zigzag import *
from jpeg.compression import *
from jpeg.dictionary_util import *
from jpeg.decompression import *
from jpeg.image_scaling import *

import time


def write_file(arr, name):
    f = open(name + '.txt', 'w')

    h, w = arr.shape

    for i in range(h):
        for j in range(w):
            f.write(str(arr[i, j]) + '\t')
        f.write('\n')

    f.close()


# load image

image = Image.open("../Examples/marbles.bmp").convert('YCbCr')
image = np.array(image)

h, w = image.shape[0], image.shape[1]

y = image[:, :, 0]
cr = image[:, :, 1]
cb = image[:, :, 2]

y = Image.fromarray(y)
cr = Image.fromarray(cr)
cb = Image.fromarray(cb)

new_image = Image.merge('YCbCr', (y, cr, cb))

image_gray = color.gray2rgb(y).astype(np.uint8)

image_gray = np.clip(image_gray, 0, 255)

image_gray = color.gray2rgb(cr).astype(np.uint8)

image_gray = np.clip(image_gray, 0, 255)

image_gray = color.gray2rgb(cb).astype(np.uint8)

image_gray = np.clip(image_gray, 0, 255)

# image = resize_image(image)

start = time.time()
out = image_compression(image)
print("LEN OUT --", len(out))
end = time.time()
print(end - start)

y = decompress(out[0], False)
cr = decompress(out[1], False)
cb = decompress(out[2], False)

y = y[:h, :w]

image_gray = color.gray2rgb(y).astype(np.uint8)

image_gray = np.clip(image_gray, 0, 255)

cr = upscale(cr, 2)
cr = cr[:h, :w]

cb = upscale(cb, 2)
cb = cb[:h, :w]

image = np.zeros((h, w, 3)).astype(np.uint8)
image[:, :, 0] = y.astype(np.uint8)
image[:, :, 1] = cr.astype(np.uint8)
image[:, :, 2] = cb.astype(np.uint8)

image = Image.fromarray(image, mode='YCbCr')
print(image.mode)
image = image.convert('RGB')

image.save("decompressed.jpg")
print("decompression done!")
