from skimage import color

from encoding.huffman import *
from encoding.rle import find_eob, run_length_encoder
from jpeg.dct import *
from jpeg.image_util import *
from jpeg.zigzag import *
from jpeg.dictionary_util import *

# load image

image = imread("../Examples/miner.jpg")
image = (color.rgb2gray(image) * 255).astype(int)
height, width = image.shape
print(image[:8, :8])

# resize image
image = resize_image(image)
height, width = image.shape

# quantize
image = image - 128

# dct image
image_dct = dct_image(image)
print(image_dct[len(image_dct) - 1])

# zigzag
zigzag_arr = []
for elem in image_dct:
    zigzag_arr.append(zigzag(elem))

# run length
rle_array = []
for elem in zigzag_arr:
    eob = find_eob(elem)
    eob = run_length_encoder(eob)
    rle_array.append(eob)

rle_array = [element for sublist in rle_array for element in sublist]

# array to string
rle_string = "".join(rle_array)

# huffman string to arr
huff_arr = str_to_array(rle_string)
# print(huff_arr)

# huff frequency
rle_freq = get_freq_dict(rle_array)
huff_freq = get_freq_dict(huff_arr)

# huffman tree
rle_huff = find_huffman(rle_freq)
huff_huff = find_huffman(huff_freq)

# print("rle -", len(rle_huff))
# print("rle2 -", len(huff_huff))

# decoding
print(len(rle_array))
rle_code = ''
for elem in rle_array:
    rle_code += rle_huff[elem]

print("rle_code -", len(rle_code))

huff_code = ''
for elem in huff_arr:
    huff_code += huff_huff[elem]

print("huff_code -", len(huff_code))

# print(rle_huff)
# print(huff_huff)

rle_huff_str = str(rle_huff)
huff_huff_str = str(huff_huff)

f = open("temp/dict.txt", 'w')
f.write(rle_huff_str)
f.close()

print(rle_code[:50])

compressed_rle = compress_dict(rle_huff_str)
compressed_huff = compress_dict(huff_huff_str)

f = open("temp/dct_rle.txt", 'w')
f.write(compressed_rle)
f.close()

dimensions = str(height) + 'x' + str(width)

print(compressed_rle[:25])
compressed_rle = dimensions + compressed_rle
print(compressed_rle[:25])
binary_dict = string_to_ascii(compressed_rle)

f = open("temp/compressed.txt", 'w')

f.write(binary_dict)
f.write(rle_code)
f.close()
