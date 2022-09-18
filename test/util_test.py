import skimage.measure
from skimage.io import imread
import os

# f = open("bitstring.dat", 'w')
# 
# f.write('1100101')
# 
# f.close()


f = open('C:/Users/ll160389d/Desktop/rle.txt', 'r')
s = f.read()
f.close()

s_arr = s[1:-1]
s_arr = s_arr.replace('(', "")
s_arr = s_arr.replace(')', "")

arr = s_arr.split(',')

print(arr[:20])
print(arr[:20:2])
arr = arr[::2]

sum = 0
for e in arr:
    sum += int(e)

print(sum)