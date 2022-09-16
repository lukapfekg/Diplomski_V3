import builtins
import time
import tkinter
import tkinter as tk
import os
from multiprocessing import Pool
from os import *
from tkinter import filedialog

import numpy
import numpy as np
import skimage.metrics
from PIL import ImageTk, Image
from dahuffman import HuffmanCodec
from tkinterdnd2 import DND_FILES

# from encoding.huffman_class import make_tree, huffman_code_tree, create_huff_dict
from encoding.rle_modular import rle_modular
from gui.util_gui import calculate_size, get_histogram, write_array_to_file, convert_bits
from jpeg.compression import image_compression
from jpeg.decompression import *
from jpeg.dictionary_util import *
from jpeg.image_scaling import upscale

from skimage import measure

from gui.util_gui import calculate_size
from util.bilinear_trasformation import bilinear_interpolation
from util.dictionary_util_modular import decompress_dict_modular


class Decompression:

    def __init__(self, root, image, out):
        self.decompressed = None
        self.entropy = 0
        self.encoding = 0
        self.vertical = 0
        self.predictive = 0
        self.quant_val = 0
        self.quant = 0
        self.block_size = 0
        self.has_dct = 0
        self.image_color_space = '0'
        self.image_width = 0
        self.image_height = 0
        self.image = '11'
        self.dictionary = dict()
        self.root = root
        self.image_bin = image
        self.out = out

        bin_file = builtins.open("compressed_image_bin.dat", 'w')
        bin_file.write(self.image_bin)
        bin_file.close()

        # canvas
        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg="#263D42")

        # info frame
        self.frame = tk.Frame(self.canvas, bg="#354552")
        self.frame.place(relheight=0.62, relwidth=0.6, relx=0.025, rely=0.25)

        self.read_file()
        print("image bin len: ", len(self.image_bin))

        # labels
        self.img_height = "Height: " + str(self.image_height)
        self.label1 = tk.Label(self.frame, text=self.img_height, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label1.pack(side=tk.TOP, pady=20)

        self.img_width = "Width: " + str(self.image_width)
        self.label2 = tk.Label(self.frame, text=self.img_width, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label2.pack(side=tk.TOP, pady=20)

        self.color_space = "Color space: " + self.image_color_space
        self.label3 = tk.Label(self.frame, text=self.color_space, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label3.pack(side=tk.TOP, pady=20)

        self.dct = 'Has DCT' if self.has_dct else 'No DCT'
        self.dct = "DCT: " + self.dct
        self.label4 = tk.Label(self.frame, text=self.dct, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label4.pack(side=tk.TOP, pady=20)

        if self.has_dct:
            self.dct = "DCT: " + self.dct
            self.label5 = tk.Label(self.frame, text='Block size: ' + str(self.block_size) + 'x' + str(self.block_size),
                                   justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
            self.label5.pack(side=tk.TOP, pady=20)

        self.label6 = tk.Label(self.frame, text='Quantization: ' + str(self.quant), justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label6.pack(side=tk.TOP, pady=20)

        if self.quant_val != 0:
            self.label7 = tk.Label(self.frame, text='Quantization value: ' + str(self.quant_val), justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
            self.label7.pack(side=tk.TOP, pady=20)

        self.label8 = tk.Label(self.frame, text='Encoding: ' + str(self.encoding), justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label8.pack(side=tk.TOP, pady=20)

        # drop-down frame
        self.button_frame = tk.Frame(self.canvas, bg="#354552")
        self.button_frame.place(relwidth=0.2, relheight=0.2, relx=0.79, rely=0.3)

        button_dropdown = tk.Button(self.button_frame, text="Decompress", height=5, width=25, fg="white", bg="#263D42")
        button_dropdown.configure(command=self.decompress)
        button_dropdown.pack(side=tk.BOTTOM, pady=10)

        self.canvas.pack()

    def read_file(self):
        params, image = get_compression_parameters(self.image_bin)
        dictionary, image = get_dictionary(image)

        self.dictionary = dictionary
        self.image = image
        self.parse_params(params)

    def parse_params(self, params):
        param_list = params.split(';')[:-1]

        # image
        self.image_height = param_list[0].split('x')[0]
        self.image_width = param_list[0].split('x')[1]
        self.image_color_space = 'RBG' if param_list[1] == 'R' else ('YCbCr444' if param_list[1] == '4' else 'YCbCr420')

        # dct
        self.has_dct = param_list[2] != '0'
        self.block_size = 16 if param_list[2] == '6' else int(param_list[2])

        self.quant = param_list[3] != 'N'
        self.quant_val = 0 if (not self.quant or param_list[3] == 'T') else int(param_list[3])

        self.predictive = param_list[4] != 'N'
        self.vertical = param_list[4] == 'V'

        self.encoding = "RLE + Entropy" if param_list[5] == 'R' else "Entropy"

    def decompress(self):

        if 'RLE' in self.encoding:
            # Has DC values
            # Has EOL
            # Counts zeros in between

            # get rle arrays from bin array
            zigzag = self.from_bit_array_to_zigzag(self.image)

            zigzag1, zigzag2, zigzag3 = self.get_images(zigzag)

            if self.has_dct:

                # recreate dct image
                # inverse zig-zag

                inverse_zigzag1 = inverse_zigzag_optimized(zigzag1, self.block_size)
                inverse_zigzag2 = inverse_zigzag_optimized(zigzag2, self.block_size)
                inverse_zigzag3 = inverse_zigzag_optimized(zigzag3, self.block_size)

                if self.predictive:
                    # inverse predictive
                    curr = 0
                    for i in range(inverse_zigzag1):
                        if i != 0:
                            inverse_zigzag1[i][0, 0] = curr - inverse_zigzag1[i][0, 0]

                        curr = inverse_zigzag1[i][0, 0]

                    for i in range(inverse_zigzag2):
                        if i != 0:
                            inverse_zigzag2[i][0, 0] = curr - inverse_zigzag2[i][0, 0]

                        curr = inverse_zigzag2[i][0, 0]

                    for i in range(inverse_zigzag3):
                        if i != 0:
                            inverse_zigzag3[i][0, 0] = curr - inverse_zigzag3[i][0, 0]

                        curr = inverse_zigzag3[i][0, 0]

                if self.quant:
                    # inverse quantization
                    inverse_zigzag1 = self.inverse_quantization(inverse_zigzag1)
                    inverse_zigzag2 = self.inverse_quantization(inverse_zigzag2)
                    inverse_zigzag3 = self.inverse_quantization(inverse_zigzag3)

                # inverse dct
                # image += 128

                image1 = self.inverse_dct(inverse_zigzag1)
                image2 = self.inverse_dct(inverse_zigzag2, False)
                image3 = self.inverse_dct(inverse_zigzag3, False)

                if '420' in self.color_space:
                    image2 = bilinear_interpolation(image2, 2)
                    image3 = bilinear_interpolation(image3, 2)

                image1 = image1[:int(self.image_height), :int(self.image_width)]
                image2 = image2[:int(self.image_height), :int(self.image_width)]
                image3 = image3[:int(self.image_height), :int(self.image_width)]

                image = np.zeros((int(self.image_height), int(self.image_width), 3)).astype(np.uint8)
                image[:, :, 0] = image1.astype(np.uint8)
                image[:, :, 1] = image2.astype(np.uint8)
                image[:, :, 2] = image3.astype(np.uint8)

                original = Image.open("../Examples/miner.jpg").convert(
                    'YCbCr') if 'Y' in self.image_color_space else Image.open("../Examples/miner.jpg")
                original = np.array(original)

                print("----PSNR----")

                psnr_orig = skimage.metrics.peak_signal_noise_ratio(original, original)
                print(psnr_orig)
                psnr = skimage.metrics.peak_signal_noise_ratio(original, image)
                print(psnr)

                image = Image.fromarray(image, mode='YCbCr') if 'Y' in self.image_color_space else Image.fromarray(
                    image, mode='RGB')
                print(image.mode)
                # image = image.convert('RGB')

                image.save("decompressed.jpg")

                # resize to original size (e.g. 1200x796 image=image[:12000, :796])

                aa = 7
            else:
                # Counts occurrences of a pixel
                # get array of pixels

                if self.vertical:
                    # create vertical image
                    aa = 5
                else:
                    # create horizontal image
                    aa = 5

                if self.predictive:
                    # inverse predictive
                    aa = 4

                if self.quant:
                    # inverse quantization
                    aa = 4

                aa = 8

            aa = 5

        elif 'Entropy' in self.encoding:
            # Counts occurrences of a pixel
            # get array of pixels

            # create vertical image

            if self.predictive:
                # inverse predictive
                aa = 4

            if self.quant:
                # inverse quantization
                aa = 4

            aa = 5

        self.decompressed = None

    def from_bit_array_to_zigzag(self, bit_array):
        keys = list(self.dictionary.keys())
        values = list(self.dictionary.values())

        curr = ''
        out = []
        out_array = []
        for i in range(len(self.image)):
            curr += self.image[i]

            if curr in values:
                temp = keys[values.index(curr)]

                if ',' in temp:
                    temp = temp[1:-1]
                    l = temp.split(',')[0]
                    r = temp.split(',')[1]

                    out_temp = ['0' for _ in range(int(l))] if int(l) > 0 else []
                    out_temp.append(r)

                    out += out_temp

                    if len(out) == self.block_size ** 2:
                        out_array.append(out)
                        out = []

                elif temp == 'E':
                    temp = ['0' for _ in range(self.block_size ** 2 - len(out))]
                    out += temp
                    out_array.append(out)
                    out = []

                else:
                    out.append(temp)

                curr = ''

        return out_array

    def get_images(self, zigzag):
        h = int(self.image_height)
        w = int(self.image_width)

        if self.has_dct:
            h += 0 if h % self.block_size == 0 else self.block_size - h % self.block_size
            w += 0 if w % self.block_size == 0 else self.block_size - w % self.block_size

        image1 = zigzag[:int(h * w // self.block_size ** 2)]
        zigzag = zigzag[int(h * w // self.block_size ** 2):]

        if '0' in self.color_space:
            h = int(np.ceil(int(self.image_height) / 2))
            w = int(np.ceil(int(self.image_width) / 2))
            h += 0 if h % self.block_size == 0 else self.block_size - h % self.block_size
            w += 0 if w % self.block_size == 0 else self.block_size - w % self.block_size

        image2 = zigzag[:int(h * w // self.block_size ** 2)]
        zigzag = zigzag[int(h * w // self.block_size ** 2):]
        image3 = zigzag[:int(h * w // self.block_size ** 2)]
        zigzag = zigzag[int(h * w // self.block_size ** 2):]

        return image1, image2, image3

    def inverse_quantization(self, array):
        quant = QUANTIZATION_MATRIX if self.block_size == 8 else (
            QUANTIZATION_MATRIX_16 if self.block_size == 16 else QUANTIZATION_MATRIX_4)

        out_array = []

        for elem in array:
            out_array.append(np.multiply(elem, quant))

        return out_array

    def inverse_dct(self, array, first=True):
        h = int(self.image_height) if '0' not in self.color_space or first else int(
            np.ceil(int(self.image_height) / 2))
        w = int(self.image_width) if '0' not in self.color_space or first else int(
            np.ceil(int(self.image_width) / 2))
        h += 0 if h % self.block_size == 0 else self.block_size - h % self.block_size
        w += 0 if w % self.block_size == 0 else self.block_size - w % self.block_size

        out_image = np.zeros((h, w)).astype(int)
        k = 0
        for i in range(h // self.block_size):
            for j in range(w // self.block_size):
                tek = array[k]
                tek = fftpack.idct(fftpack.idct(tek.T, norm='ortho').T, norm='ortho').astype(int)
                tek += 128
                tek[tek < 0] = 0
                tek[tek > 255] = 255

                out_image[i * self.block_size:i * self.block_size + self.block_size,
                j * self.block_size:j * self.block_size + self.block_size] = tek

                k += 1

        return out_image


def get_compression_parameters(bit_array):
    curr = ''

    out_array = ''
    while curr != '{':
        temp = chr(int(str(bit_array[:8]), 2))

        if temp == '{':
            break

        bit_array = bit_array[8:]

        out_array += temp
        curr = temp

    print(out_array)
    return out_array, bit_array


def get_dictionary(bit_array):
    curr = ''
    out_array = ''

    print(len(bit_array))

    while curr != '}':
        temp = chr(int(str(bit_array[:8]), 2))
        bit_array = bit_array[8:]

        out_array += temp
        curr = temp

    print(len(bit_array))

    dictionary = decompress_dict_modular(out_array)

    dictionary_keys = dictionary.keys()
    dictionary_vals = render_values(dictionary.values())

    dictionary = {key: val for key, val in zip(dictionary_keys, dictionary_vals)}

    return dictionary, bit_array


def render_values(values):
    out_values = []

    for elem in values:
        elem = elem[1:-1]
        bits = int(elem.split(',')[0])
        value = bin(int(elem.split(',')[1]))[2:]

        l = ['0' for _ in range(bits - len(value))]
        l = "".join(l)

        out_values.append(l + value)

    return out_values


def inverse_zigzag_optimized(zigzag_array, block_size):
    out_array = np.zeros((block_size, block_size)).astype(int)

    coord = zigzag_array_coordinates_8 if block_size == 8 else (
        zigzag_array_coordinates_4 if block_size == 4 else zigzag_array_coordinates_16)

    out_list = []
    for elem in zigzag_array:
        for i, el in enumerate(elem):
            x, y = coord[i]
            out_array[x, y] = el

        out_list.append(out_array)
        out_array = np.zeros((block_size, block_size)).astype(int)

    return out_list
