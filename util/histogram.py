from collections import Counter, OrderedDict
from skimage import color
from encoding.huffman import *
from encoding.rle import find_eob, run_length_encoder
from jpeg.dct import *
from jpeg.image_util import *
from jpeg.zigzag import *
from jpeg.compression import *
from jpeg.dictionary_util import *

image = imread("../Examples/miner.jpg")

image = (color.rgb2ycbcr(image) * 255).astype(np.uint8)
image = image[:, :, 0]

print(np.min(image))
print(np.max(image))

data = Counter(image.flatten())

d = {k: d for k, d in data.items()}

d = OrderedDict(sorted(d.items()))
