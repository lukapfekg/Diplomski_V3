import numpy as np
from skimage import color
from scipy import fftpack

from encoding.huffman import *
from encoding.rle import find_eob, run_length_encoder
from jpeg.dct import *
from jpeg.image_util import *
from jpeg.zigzag import *
from jpeg.dictionary_util import *

###############################################
image = imread("../Examples/miner.jpg")
image = (color.rgb2gray(image) * 255).astype(int)
height, width = image.shape
print(image[:8, :8])
############################################################

f = open("temp/compressed.txt", 'r')
compressed = f.readline()
f.close()

print(len(compressed))

# dimensions
prev = '.'
i = 0
inp = []
s = ""
while 1:
    temp = chr(int(str(compressed[i * 8:i * 8 + 8]), 2))

    if temp == '{':
        inp.append(int(s))
        break
    elif temp == 'x':
        inp.append(int(s))
        s = ''
        i += 1
    else:
        s += temp
        prev = temp
        i += 1

h, w = inp

new_h = h + h % 8
new_w = w + w % 8

compressed = compressed[i * 8:]

# build dictionary
dictionary, pos = binary_to_dict(compressed)

compressed = compressed[pos:]
# convert code
temp = ''
vals = list(dictionary.values())
out = []
for c in compressed:
    temp += c
    if temp in vals:
        out.append(list(dictionary.keys())[vals.index(temp)])
        temp = ''

# create dct arrays
dct_array = []
temp = []

for elem in out:
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

for elem in dct_array:
    if len(elem) != 64:
        print(True)

# inverse zigzag
inv_zigzag = []
for elem in dct_array:
    inv_zigzag.append(inverse_zigzag(elem))

# create image
h_len = new_h // 8
w_len = new_w // 8
dct_image = np.zeros((new_h, new_w))
k = 0
for i in range(h_len):
    for j in range(w_len):
        dct_image[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = inv_zigzag[k]
        k += 1

image = np.zeros((new_h, new_w))
# inverse dct
for i in range(h_len):
    for j in range(w_len):
        temp = dct_image[i * 8:i * 8 + 8, j * 8:j * 8 + 8]
        tek = np.multiply(temp, QUANTIZATION_MATRIX).astype(int)
        tek = fftpack.idct(fftpack.idct(tek.T, norm='ortho').T, norm='ortho').astype(int)
        tek += 128

        image[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = tek


imsave("miner_decompressed.jpg", image)
# build an image
