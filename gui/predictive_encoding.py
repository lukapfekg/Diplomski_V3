import tkinter
import tkinter as tk
import os
from multiprocessing import Pool
from os import *
from tkinter import filedialog

import numpy as np
from PIL import ImageTk, Image
from tkinterdnd2 import DND_FILES

from gui.util_gui import calculate_size, get_histogram, write_array_to_file, convert_bits
from jpeg.compression import image_compression
from jpeg.decompression import *
from jpeg.dictionary_util import *
from jpeg.image_scaling import upscale

from gui.util_gui import calculate_size


class PredictiveEncoding:

    def __init__(self, root, img1, img2, img3, out):
        self.root = root
        self.image1 = img1
        self.image2 = img2
        self.image3 = img3
        self.out = out
        self.has_dct = self.out[-2] != '0'
        self.block_size = 16 if self.out[-2] == '6' else int(self.out[-2])

        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg="#263D42")

        # drop-down frame
        self.button_frame = tk.Frame(self.canvas, bg="#354552")
        self.button_frame.place(relwidth=0.2, relheight=0.2, relx=0.79, rely=0.3)

        button_dropdown = tk.Button(self.button_frame, text="Choose", height=5, width=25, fg="white", bg="#263D42")
        button_dropdown.configure(command=self.accept_DCT)
        button_dropdown.pack(side=tk.BOTTOM, pady=10)

        self.canvas.pack()

    def accept_DCT(self):
        print('usloooo')