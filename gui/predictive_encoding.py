import tkinter
import tkinter as tk
import os
from multiprocessing import Pool
from os import *
from tkinter import filedialog

import numpy as np
from PIL import ImageTk, Image
from tkinterdnd2 import DND_FILES

from gui.RLE_and_Enthropy import RleAndEntropy
from gui.util_gui import calculate_size, get_histogram, write_array_to_file, convert_bits
from jpeg.compression import image_compression
from jpeg.decompression import *
from jpeg.dictionary_util import *
from jpeg.image_scaling import upscale

from skimage import measure

from gui.util_gui import calculate_size
from util.bilinear_trasformation import bilinear_interpolation


class PredictiveEncoding:

    def __init__(self, root, img1, img2, img3, out):
        self.entropy = None
        self.root = root
        self.image1 = img1
        self.image2 = img2
        self.image3 = img3
        self.out = out
        self.list_out = self.out.split(';')
        self.has_dct = self.list_out[2] != '0'
        self.block_size = 16 if self.list_out[2] == '6' else int(self.list_out[2])

        self.img_height, self.img_width = self.list_out[0].split('x')
        self.color_space = 'RBG' if self.list_out[1] == 'R' else ('YCbCr444' if self.list_out[1] == '4' else 'YCbCr420')
        self.dct = 'Has DCT' if self.has_dct else 'Does not have DCT'
        self.quant = self.list_out[3] != 'N'
        self.quant_val = 0 if (not self.quant or self.list_out[3] == 'T') else int(self.list_out[3])

        self.calc_entropy()

        # canvas
        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg="#263D42")

        # info frame
        self.frame = tk.Frame(self.canvas, bg="#354552")
        self.frame.place(relheight=0.62, relwidth=0.6, relx=0.025, rely=0.25)

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

        self.label6 = tk.Label(self.frame, text='Quantization: ' + str(self.quant), justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label6.pack(side=tk.TOP, pady=20)

        if self.quant_val != 0:
            self.label7 = tk.Label(self.frame, text='Quantization value: ' + str(self.quant_val), justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
            self.label7.pack(side=tk.TOP, pady=20)

        self.label8 = tk.Label(self.frame, text='Entropy: ' + str(self.entropy), justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label8.pack(side=tk.TOP, pady=20)

        # drop-down frame
        self.button_frame = tk.Frame(self.canvas, bg="#354552")
        self.button_frame.place(relwidth=0.325, relheight=0.3, relx=0.65, rely=0.3)

        self.options1 = ["YES", "NO"]
        self.clicked1 = tk.StringVar()
        self.clicked1.set("NO")
        # self.clicked1.set("Do predictive encoding")

        self.drop = tk.OptionMenu(self.button_frame, self.clicked1, *self.options1)
        self.drop.config(width=40, font=("Roboto", 18, "bold"), foreground="#FFFFFF", background="#263D42")
        self.drop.pack(side=tk.TOP, pady=10)

        if not self.has_dct:
            self.options2 = ["Horizontal", "Vertical"]
            self.clicked2 = tk.StringVar()
            self.clicked2.set("Choose quantization parameter")

            self.drop2 = tk.OptionMenu(self.button_frame, self.clicked2, *self.options2)
            self.drop2.config(width=40, font=("Roboto", 18, "bold"), foreground="#FFFFFF", background="#263D42")
            self.drop2.pack(side=tk.TOP, pady=10)

        button_dropdown = tk.Button(self.button_frame, text="Choose", height=5, width=25, fg="white", bg="#263D42")
        button_dropdown.configure(command=self.accept_DCT)
        button_dropdown.pack(side=tk.BOTTOM, pady=10)

        self.canvas.pack()

    def accept_DCT(self):
        print("-PREDICTIVE-")
        if self.clicked1.get() == 'YES':
            if self.has_dct:
                # print(self.image1[25*8: 25*8+8, :8])
                img1 = self.dct_predictive_encoding(self.image1)
                img2 = self.dct_predictive_encoding(self.image2)
                img3 = self.dct_predictive_encoding(self.image3)

                self.out += 'T;'
                self.canvas.destroy()
                RleAndEntropy(self.root, img1, img2, img3, self.out)

            else:
                if self.clicked2.get() == "Horizontal":
                    img1 = self.predictive_encoding(self.image1, 'h')
                    img2 = self.predictive_encoding(self.image2, 'h')
                    img3 = self.predictive_encoding(self.image3, 'h')

                    self.out += 'H;'
                    self.canvas.destroy()
                    RleAndEntropy(self.root, img1, img2, img3, self.out)

                elif self.clicked2.get() == 'Vertical':
                    img1 = self.predictive_encoding(self.image1, 'h')
                    img2 = self.predictive_encoding(self.image2, 'h')
                    img3 = self.predictive_encoding(self.image3, 'h')

                    self.out += 'V;'
                    self.canvas.destroy()
                    RleAndEntropy(self.root, img1, img2, img3, self.out)

        else:
            self.out += 'N;'
            self.canvas.destroy()
            RleAndEntropy(self.root, self.image1, self.image2, self.image3, self.out)
            # next screen self.image1,2,3 is sent

    def predictive_encoding(self, image, axis):
        h, w = image.shape

        out_image = np.array(image)

        prev = 0

        h_info = h if axis == 'h' else w
        w_info = w if axis == 'v' else h

        for i in range(h if axis == 'h' else w):
            for j in range(w if axis == 'h' else h):
                if i == 0 and j == 0:
                    prev = image[i, j]
                    continue

                if axis == 'h':
                    out_image[i, j] = image[i, j] - prev
                    prev = image[i, j]
                else:
                    out_image[j, i] = image[j, i] - prev
                    prev = image[j, i]

        return out_image

    def dct_predictive_encoding(self, image):
        h, w = image.shape

        h = h // self.block_size
        w = w // self.block_size

        out_img = np.array(image)

        for i in range(h):
            for j in range(w):
                if i == 0 and j == 0:
                    prev = image[i * self.block_size, j * self.block_size]
                    continue

                out_img[i * self.block_size, j * self.block_size] = image[
                                                                        i * self.block_size, j * self.block_size] - prev

                prev = image[i * self.block_size, j * self.block_size]

        return out_img

    def calc_entropy(self):
        image = np.zeros((self.image1.shape[0], self.image1.shape[1], 3))
        print(image.shape)
        image[:, :, 0] = self.image1
        image[:, :, 1] = self.image2 if '420' not in self.color_space else bilinear_interpolation(self.image2, 2)
        image[:, :, 2] = self.image3 if '420' not in self.color_space else bilinear_interpolation(self.image3, 2)

        self.entropy = measure.shannon_entropy(image)
        print("entropy4:", self.entropy)
