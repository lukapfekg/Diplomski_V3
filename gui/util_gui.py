import math
from collections import Counter

import numpy as np


def calculate_size(c_width, c_height, i_width, i_height):
    if i_width <= i_height:
        odnos = c_height / i_height
    else:
        odnos = c_width / i_width

    w = round(np.ceil(odnos * i_width))
    h = round(np.ceil(odnos * i_height))

    return w, h


def get_histogram(image):
    data = Counter(image)

    output = {k: d for k, d in data.items()}

    return list(output.keys()), list(output.values())


def write_array_to_file(arr, name):
    f = open(name + ".txt", 'w')
    f.write(str(arr))
    f.close()


def convert_bits(bits):
    size_name = ['B', 'KB', 'MB', 'GB']
    i = int(math.log(bits, 1024))
    res = round(bits / math.pow(1024, i), 2)
    return f"{res}{size_name[i]}"


