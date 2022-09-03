import skimage.measure
from skimage.io import imread

filenames = ["../Examples/miner.jpg", "temp/decompressed.jpg"]

img = imread(filenames[0])
entropy = skimage.measure.shannon_entropy(img)
print(entropy)

img = imread(filenames[1])
entropy = skimage.measure.shannon_entropy(img)
print(entropy)


