import time

from jpeg.decompression import *

# load image
f = open("compressed.txt", 'r')
bit_array = f.readline()
f.close()

start = time.time()
out = decompress(bit_array)
end = time.time()

print(end - start)
