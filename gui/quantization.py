import tkinter
import tkinter as tk
import os
from multiprocessing import Pool
from os import *
from tkinter import filedialog

import numpy as np
import skimage.measure
from PIL import ImageTk, Image
from tkinterdnd2 import DND_FILES

from gui.predictive_encoding import PredictiveEncoding
from gui.util_gui import calculate_size, get_histogram, write_array_to_file, convert_bits
from jpeg.compression import image_compression
from jpeg.decompression import *
from jpeg.dictionary_util import *
from jpeg.image_scaling import upscale

from gui.util_gui import calculate_size
from util.bilinear_trasformation import bilinear_interpolation


class QuantizeImage:

    def __init__(self, root, img1, img2, img3, out, filename):
        self.filename = filename
        self.quant = None
        self.root = root
        self.image1 = img1.astype(int)
        self.image2 = img2.astype(int)
        self.image3 = img3.astype(int)
        self.out = out
        self.list_out = self.out.split(';')
        self.has_dct = self.list_out[2] != '0'
        self.block_size = 16 if self.list_out[2] == '6' else int(self.list_out[2])
        self.entropy = 0

        self.img_height, self.img_width = self.list_out[0].split('x')
        self.color_space = 'RBG' if self.list_out[1] == 'R' else ('YCbCr444' if self.list_out[1] == '4' else 'YCbCr420')
        self.dct = 'Has DCT' if self.has_dct else 'Does not have DCT'

        self.calc_entropy()

        # canvas
        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg="#263D42")

        # info frame
        self.frame = tk.Frame(self.canvas, bg="#354552")
        self.frame.place(relheight=0.55, relwidth=0.6, relx=0.025, rely=0.25)

        # labels
        self.img_height = "Height: " + self.img_height
        self.label1 = tk.Label(self.frame, text=self.img_height, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label1.pack(side=tk.TOP, pady=20)

        self.img_width = "Width: " + self.img_width
        self.label2 = tk.Label(self.frame, text=self.img_width, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label2.pack(side=tk.TOP, pady=20)

        self.color_space = "Color space: " + self.color_space
        self.label3 = tk.Label(self.frame, text=self.color_space, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label3.pack(side=tk.TOP, pady=20)

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

        self.label6 = tk.Label(self.frame, text='Entropy: ' + str(self.entropy),
                               justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label6.pack(side=tk.TOP, pady=20)

        # drop-down frame
        self.button_frame = tk.Frame(self.canvas, bg="#354552")
        self.button_frame.place(relwidth=0.325, relheight=0.3, relx=0.65, rely=0.3)

        self.options1 = ["YES", "NO"]
        self.clicked1 = tk.StringVar()
        self.clicked1.set("YES")
        # self.clicked1.set("Quantize image")

        self.drop = tk.OptionMenu(self.button_frame, self.clicked1, *self.options1)
        self.drop.config(width=40, font=("Roboto", 18, "bold"), foreground="#FFFFFF", background="#263D42")
        self.drop.pack(side=tk.TOP, pady=10)

        if not self.has_dct:
            self.options2 = ["2", "4", "8"]
            self.clicked2 = tk.StringVar()
            self.clicked2.set("2")
            # self.clicked2.set("Choose quantization parameter")

            self.drop2 = tk.OptionMenu(self.button_frame, self.clicked2, *self.options2)
            self.drop2.config(width=40, font=("Roboto", 18, "bold"), foreground="#FFFFFF", background="#263D42")
            self.drop2.pack(side=tk.TOP, pady=10)

        button_dropdown = tk.Button(self.button_frame, text="Choose", height=5, width=25, fg="white", bg="#263D42")
        button_dropdown.configure(command=self.accept_DCT)
        button_dropdown.pack(side=tk.BOTTOM, pady=10)

        self.canvas.pack()

    def accept_DCT(self):
        if self.clicked1.get() == 'YES':
            if self.has_dct:
                img1 = quantize_images(self.image1, self.block_size).astype(int)
                img2 = quantize_images(self.image2, self.block_size).astype(int)
                img3 = quantize_images(self.image3, self.block_size).astype(int)

                self.out += 'T;'

                self.canvas.destroy()
                PredictiveEncoding(self.root, img1, img2, img3, self.out, self.filename)

            else:
                if self.clicked2.get() in self.options2:
                    self.quant = int(self.clicked2.get())

                    img1 = np.divide(self.image1, self.quant).astype(int)
                    img2 = np.divide(self.image2, self.quant).astype(int)
                    img3 = np.divide(self.image3, self.quant).astype(int)

                    self.out += self.clicked2.get() + ';'

                    self.canvas.destroy()
                    PredictiveEncoding(self.root, img1, img2, img3, self.out, self.filename)
        elif self.clicked1.get() == 'NO':
            self.out += 'N;'
            self.canvas.destroy()
            PredictiveEncoding(self.root, self.image1, self.image2, self.image3, self.out, self.filename)

    def calc_entropy(self):
        image = np.zeros((self.image1.shape[0], self.image1.shape[1], 3))

        image[:, :, 0] = self.image1
        image[:, :, 1] = self.image2 if '420' not in self.color_space else bilinear_interpolation(self.image2, 2)[
                                                                           :self.image1.shape[0], :self.image1.shape[1]]
        image[:, :, 2] = self.image3 if '420' not in self.color_space else bilinear_interpolation(self.image3, 2)[
                                                                           :self.image1.shape[0], :self.image1.shape[1]]

        self.entropy = skimage.measure.shannon_entropy(image)
        print("entropy3:", self.entropy)


def quantize_images(image, block_size):
    out_image = np.zeros((image.shape[0], image.shape[1]))

    blocks_h = image.shape[0] // block_size
    blocks_w = image.shape[1] // block_size

    quant = QUANTIZATION_MATRIX if block_size == 8 else (
        QUANTIZATION_MATRIX_16 if block_size == 16 else QUANTIZATION_MATRIX_4)

    for i in range(blocks_h):
        for j in range(blocks_w):
            out_image[i * block_size: i * block_size + block_size, j * block_size:j * block_size + block_size] \
                = np.divide(
                image[i * block_size: i * block_size + block_size, j * block_size:j * block_size + block_size], quant)

    return out_image
