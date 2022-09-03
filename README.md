# Implementation of JPEG algorithm

## Compression flow
- Input image is converted to YCbCr color space
- Y
  - Image is firstly resized so its height and width is divisible by 8 (for dct 8x8 blocks)
  - Implemented DCT to an image. Image is now converted to a list of 8x8 pixel blocks 
  - Using zigzag pattern image is converted to list of one dimensional arrays
  - RLE is applied on each array, image now is represented as one array
  - Huffman coding is applied to that array, and we transform RLE array to byte code
  - As we need to save information about original dimensions of and image and huffman coding dictionary, ascii representation of characters is used, and put at the start of a coded message
  - Then we add transformed byte code to the end of a coded message
- CbCr
  - Before we resize the image to be divisible by 8, we resize it to the half of its size
  - Then we follow the same steps as for Y color component

## Decompression flow
- Y
  - We retrieve the original dimensions of an image
  - After we retrieve huffman dictionary, and rebuild it
  - The rest of byte code is converted to an RLE array using rebuilt dictionary
  - Using inverse RLE we get our DCT arrays
  - Using inverse zigzag algorithm we get DCT 8x8 blocks
  - Using inverse DCT we get compressed image
- CbCr
  - Same steps as Y
  - After that we need to increase size of Cb and Cr planes to match original size

## RLE
It differs from original JPEG algorithm as we count the number of occurrences of the number, rather than occurences of zeros befoe the number.<br>
e.g. 0 0 0 2 2 2 -> (2, 0), (2, 2), as per (3, 2), (0, 2), (0, 2)<br>
EOL character is 'E'
DC component of DCT is represented as is

## Huffman coding
Huffman coding is, I would say, standard. Coded values are: DC component (integer), EOL character('E') or RLE component(e.g. (3, 2)).
For compression purposes, before writing to output code, huffman dictionary is reduced.<br>
e.g. {'-63':'101', 'E':'1101', '(0, 1)':'11101'} -> {-63:101,E:1101,(0,1):11101} 