import time

from skimage import color

from encoding.huffman import *
from encoding.huffman_class import *
from encoding.rle import *
from jpeg.dct import *
from jpeg.dictionary_util import *
from jpeg.image_util import *
from jpeg.zigzag import *
from jpeg.image_scaling import *

import threading
from multiprocessing.pool import ThreadPool


def write_file(arr, name, dim=2):
    f = open("../temp/" + name + '.txt', 'w')

    if dim == 2:
        h, w = arr.shape

        for i in range(h):
            for j in range(w):
                f.write(str(arr[i, j]) + '\t')
            f.write('\n')

        f.close()

    else:
        for i in range(len(arr)):
            f.write(str(arr[i]) + '\n')
        f.close()


# region compression

def compress(image, lossless=False):
    # get original height and width
    height, width = image.shape

    # resize image for 8x8 blocks
    image_resized = resize_image(image)
    new_h, new_w = image_resized.shape

    # quantization and dct
    image_resized -= 128
    image_dct = dct_image(image_resized, lossless)

    # for every dct block get zigzag array
    zigzag_array = get_zigzag_optimized(image_dct)

    # run length compression
    rle_array = find_rle(zigzag_array, 1)

    # find huff frequency
    freq = get_freq_dict(rle_array)
    print(freq)

    # find huff tree
    huff = find_huffman(freq)
    # print(huff)

    # convert dct array to huffman code
    huff_code = ''
    for elem in rle_array:
        if elem != '-63' or elem != 'E':
            s = 0
        huff_code += huff[elem]

    # compress huff dict
    compressed_huff = compress_dict(str(huff))

    # convert dimensions and dict to binary ascii code
    dimensions = str(height) + "x" + str(width)
    compressed_huff = dimensions + compressed_huff
    binary_huff = string_to_ascii(compressed_huff)

    huff_code = binary_huff + huff_code

    return huff_code


def image_compression(image, lossless=False):
    if len(image.shape) == 2:
        out_image = compress(image, lossless)
        h, w = image.shape
        print("compression rate:", h * w * 8 / len(out_image))

        f = open("compressed.txt", 'w')
        f.write(out_image)
        f.close()

        return out_image

    else:

        y = image[:, :, 0]
        cr = image[:, :, 1]
        cb = image[:, :, 2]

        out_image = []
        siz = 0
        out_image.append(compress(y))
        siz += len(out_image[0])
        out_image.append(compress(rescale_image(cr, 2)))
        siz += len(out_image[1])
        out_image.append(compress(rescale_image(cb, 2)))
        siz += len(out_image[2])
        height, width, planes = image.shape
        print("size after compression :", siz)
        print("compression rate:", height * width * planes * 8 / siz)

        return out_image


# endregion

# region decompression

def decompress(bit_array, save_image=True):
    # extract dimensions
    without_dimensions_arr, h, w = get_dimensions(bit_array)
    new_h = h + h % 8
    new_w = w + w % 8

    # get dictionary
    dictionary, pos = binary_to_dict(without_dimensions_arr)

    # cut string to get only huffman code
    huff_code = without_dimensions_arr[pos:]

    # get rle array
    rle_array = get_array_from_huff(huff_code, dictionary)

    # get dct array
    dct_array = get_dct_array_from_rle(rle_array)

    # recreate 8x8 blocks
    inv_zigzag = []
    for elem in dct_array:
        inv_zigzag.append(inverse_zigzag(elem))

    # recreate image
    image = recreate_image(inv_zigzag, new_h, new_w)

    if save_image:
        image = color.gray2rgb(image).astype(int)
        image = np.clip(image, 0, 255)
        image = image.astype(np.uint8)
        image = image[:h, :w]

        imsave("decompressed.jpg", image)
        print("decompression done!")
        return None

    else:
        return image.astype(np.uint8)


def get_dimensions(bit_array):
    i = 0
    inp = []
    s = ""
    while 1:
        temp = chr(int(str(bit_array[i * 8:i * 8 + 8]), 2))

        if temp == '{':
            inp.append(int(s))
            break
        elif temp == 'x':
            inp.append(int(s))
            s = ''
            i += 1
        else:
            s += temp
            i += 1

    h, w = inp

    return bit_array[i * 8:], h, w


def get_array_from_huff(bit_string, dictionary):
    temp = ''
    vals = list(dictionary.values())
    out = []
    for c in bit_string:
        temp += c
        if temp in vals:
            out.append(list(dictionary.keys())[vals.index(temp)])
            temp = ''

    return out


def get_dct_array_from_rle(rle_array):
    dct_array = []
    temp = []

    for elem in rle_array:
        if elem == 'E':
            temp.append(0)
            arr_len = len(temp)
            for i in range(64 - arr_len):
                temp.append(0)

            dct_array.append(temp)
            temp = []
        elif ',' in elem:
            curr = elem.replace("(", "")
            curr = curr.replace(")", "")
            curr = curr.split(",")
            curr = [int(c) for c in curr]
            for i in range(curr[0] + 1):
                temp.append(curr[1])
        else:
            temp.append(int(elem))

    return dct_array


def recreate_image(zigzag_array, new_h, new_w, lossless=False):
    h_len = new_h // 8
    w_len = new_w // 8
    dct_image = np.zeros((new_h, new_w))
    k = 0
    for i in range(h_len):
        for j in range(w_len):
            dct_image[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = zigzag_array[k]
            k += 1

    image = np.zeros((new_h, new_w))
    # inverse dct
    for i in range(h_len):
        for j in range(w_len):
            tek = dct_image[i * 8:i * 8 + 8, j * 8:j * 8 + 8]
            if not lossless:
                tek = np.multiply(tek, QUANTIZATION_MATRIX).astype(int)
            tek = fftpack.idct(fftpack.idct(tek.T, norm='ortho').T, norm='ortho').astype(int)
            tek += 128

            tek[tek < 0] = 0
            tek[tek > 255] = 255

            image[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = tek

    return image


def median_block(single_block):
    resized = np.zeros((10, 10))
    resized[1:-1, 1:-1] = single_block

    resized[0, :] = resized[2, :]
    resized[9, :] = resized[7, :]
    resized[:, 0] = resized[:, 2]
    resized[:, 9] = resized[:, 7]

    i, j = np.where(resized[1:-1, 1:-1] > 250)
    i += 1
    j += 1

    for k in range(len(i)):
        resized[i[k], j[k]] = np.median(resized[i[k] - 1:i[k] + 2, j[k] - 1: j[k] + 2])

    return resized[1:-1, 1:-1]
# endregion
