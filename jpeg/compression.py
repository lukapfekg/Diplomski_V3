from skimage import color

from encoding.huffman import *
from encoding.rle import *
from jpeg.dct import *
from jpeg.dictionary_util import *
from jpeg.image_util import *
from jpeg.zigzag import *
from jpeg.image_scaling import *


def write_file(arr, name):
    f = open("../temp/" + name + '.txt', 'w')

    h, w = arr.shape

    for i in range(h):
        for j in range(w):
            f.write(str(arr[i, j]) + '\t')
        f.write('\n')

    f.close()


def compress(image):
    # get original height and width
    height, width = image.shape

    # resize image for 8x8 blocks
    image_resized = resize_image(image)
    new_h, new_w = image_resized.shape

    # quantization and dct
    image_resized -= 128
    image_dct = dct_image(image_resized)

    # for every dct block get zigzag array
    zigzag_array = get_zigzag_optimized(image_dct)
    # zigzag_array = get_zigzag_array(image_dct)

    # run length compression
    rle_array = find_rle(zigzag_array, 1)

    # find huff frequency
    freq = get_freq_dict(rle_array)

    # find huff tree
    huff = find_huffman(freq)

    # convert dct array to huffman code
    huff_code = ''
    for elem in rle_array:
        huff_code += huff[elem]

    # compress huff dict
    compressed_huff = compress_dict(str(huff))

    # convert dimensions and dict to binary ascii code
    dimensions = str(height) + "x" + str(width)
    compressed_huff = dimensions + compressed_huff
    binary_huff = string_to_ascii(compressed_huff)

    huff_code = binary_huff + huff_code

    return huff_code


def image_compression(image):
    if len(image.shape) == 2:
        out_image = compress(image)
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
