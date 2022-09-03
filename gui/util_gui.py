import numpy as np
import itertools
import time
from collections import Counter

from PIL import ImageTk, Image

from jpeg.lossless_compression import write_file


def calculate_size(c_width, c_height, i_width, i_height):
    if i_width <= i_height:
        odnos = c_height / i_height
    else:
        odnos = c_width / i_width

    w = round(odnos * i_width)
    h = round(odnos * i_height)

    return w, h


def get_histogram(image):
    data = Counter(image)

    output = {k: d for k, d in data.items()}

    return list(output.keys()), list(output.values())


def write_array_to_file(arr, name):
    f = open(name + ".txt", 'w')
    f.write(str(arr))
    f.close()


# image = Image.open("../temp/decompressed.jpg").convert('L')
# image = np.array(image)
#
# image1 = image.flatten()
#
# keys, values = get_histogram(image1)
#
# hist = list(np.zeros(256).astype(int))
#
# for k, i in enumerate(keys):
#     hist[k] = values[i]
#
# a, b = image.shape
# print(a * b)
#
# print(sum(hist))
#
# f = open("hist.txt", 'w')
# f.write(str(hist))
# f.close()
