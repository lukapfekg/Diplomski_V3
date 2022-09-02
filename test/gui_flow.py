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


def compress_image(filename):
    # load image
    image = Image.open(filename)
    image = np.array(image)
    h, w = image.shape[0], image.shape[1]

    if len(image.shape) == 3:
        image = Image.open(filename).convert('YCbCr')
        image = np.array(image)

    # start compression
    start = time.time()
    out = image_compression(image)
    end = time.time()
    diff_compression = end - start
    print("compression time", diff_compression)

    # star decompression thread
    threading.Thread(target=decompress_image, args=[out, h, w]).start()


def decompress_image(bit_array, h ,w):
    start = time.time()

    if len(bit_array) == 3:
        y = decompress(bit_array[0], False)
        cr = decompress(bit_array[1], False)
        cb = decompress(bit_array[2], False)

        y = y[:h, :w]

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

    else:
        y = decompress(bit_array, False)
        y = y[:h, :w]

        y = color.gray2rgb(y)
        imsave("decompressed.jpg", y)

    end = time.time()
    diff_decompression = end - start
    print("decompression time", diff_decompression)


filename = "../Examples/etf_blur.tif"

compress_image(filename)

