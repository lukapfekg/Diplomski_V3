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
from bitarray import bitarray
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


class ResultWindow:

    def __init__(self, root, filename, decompressed_image, color_space, size_old, size_new):
        self.new_image = None
        self.disp_old_image = None
        self.old_image = None
        self.root = root
        self.filename = filename
        self.image_height = 675
        self.image_width = 675
        self.histo_old = None
        self.histo_new = None
        self.size_old = size_old
        self.size_new = size_new
        self.decompressed_image = decompressed_image
        self.color_space = color_space

        self.canvas = tk.Canvas(root, height=900, width=1500, bg="#263D42")

        # old image frame
        self.old_image_frame = tk.Frame(self.canvas, bg="#263D42")
        self.old_image_frame.place(relheight=0.75, relwidth=0.45, relx=0.01, rely=0.035)

        # new image frame
        self.new_image_frame = tk.Frame(self.canvas, bg="#263D42")
        self.new_image_frame.place(relheight=0.75, relwidth=0.45, relx=0.54, rely=0.035)

        # button_frame
        self.button_frame = tk.Frame(self.canvas, bg="#263D42")
        self.button_frame.place(relheight=0.15, relwidth=0.08, relx=0.46, rely=0.84)

        # image canvases
        self.old_img_canvas = tk.Canvas(self.old_image_frame, height=self.image_height, width=self.image_width,
                                        bg="#354552",
                                        bd=0,
                                        highlightthickness=0,
                                        relief='ridge')
        self.old_img_canvas.pack()
        self.new_img_canvas = tk.Canvas(self.old_image_frame, height=self.image_height, width=self.image_width,
                                        bg="#354552",
                                        bd=0,
                                        highlightthickness=0,
                                        relief='ridge')
        self.new_img_canvas.pack()

        # label frames
        self.label_frame1 = tk.Frame(self.canvas, bg="#263D42")
        self.label_frame1.place(relheight=0.02, relwidth=0.45, relx=0.01, rely=0.01)
        self.label_frame2 = tk.Frame(self.canvas, bg="#263D42")
        self.label_frame2.place(relheight=0.02, relwidth=0.45, relx=0.54, rely=0.01)

        self.label_frame3 = tk.Frame(self.canvas, bg="#263D42")
        self.label_frame3.place(relheight=0.02, relwidth=0.45, relx=0.01, rely=0.8)
        self.label_frame4 = tk.Frame(self.canvas, bg="#263D42")
        self.label_frame4.place(relheight=0.02, relwidth=0.45, relx=0.54, rely=0.8)

        # Labels
        self.image_label1 = tk.Label(self.label_frame1, text="BEFORE COMPRESSION", justify=tk.CENTER,
                                     width=80, height=1, font=("Roboto", 16, "bold"), bg="#263D42", fg="#CABAAD")
        self.image_label1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.image_label2 = tk.Label(self.label_frame2, text="AFTER COMPRESSION", justify=tk.CENTER,
                                     width=80, height=1, font=("Roboto", 16, "bold"), bg="#263D42", fg="#CABAAD")
        self.image_label2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.image_label3 = tk.Label(self.label_frame3, text=convert_bits(self.size_old), justify=tk.CENTER,
                                     width=80, height=1, font=("Roboto", 16, "bold"), bg="#263D42", fg="#CABAAD")
        self.image_label3.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.image_label4 = tk.Label(self.label_frame4, text=convert_bits(self.size_new), justify=tk.CENTER,
                                     width=80, height=1, font=("Roboto", 16, "bold"), bg="#263D42", fg="#CABAAD")
        self.image_label4.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # new compression button
        # button = tk.Button(self.button_frame, text="Return", padx=10, pady=10, fg="white", bg="#263D42")
        # button.configure(command=self.change_canvas, height=2, width=10)
        # button.pack(side=tk.BOTTOM)
        #
        # histo button
        histo_button = tk.Button(self.button_frame, text="Info", padx=10, pady=10, fg="white", bg="#263D42")
        histo_button.configure(command=self.display_images, height=2, width=10)
        # histo_button.pack(side=tk.TOP)

        self.display_images()

        self.canvas.pack()

    def display_images(self):
        self.old_img_canvas.destroy()

        self.old_image = Image.open(self.filename)
        w, h = self.old_image.size
        w, h = calculate_size(self.image_width, self.image_height, w, h)

        self.old_image = self.old_image.resize((w, h), Image.ANTIALIAS)

        self.disp_old_image = ImageTk.PhotoImage(self.old_image)
        self.old_img_canvas = tk.Canvas(self.old_image_frame, height=h, width=w, bg="gray", bd=0,
                                        highlightthickness=0,
                                        relief='ridge')
        self.old_img_canvas.create_image(0, 0, anchor=tk.NW, image=self.disp_old_image)
        self.old_img_canvas.pack()
        threading.Thread(target=self.display_new_image).start()

    def display_new_image(self):
        self.new_img_canvas.destroy()

        h, w, _ = self.decompressed_image.shape

        self.new_image = Image.fromarray(self.decompressed_image,
                                         mode='YCbCr') if 'Y' in self.color_space else Image.fromarray(
            self.decompressed_image, mode='RGB')

        w, h = calculate_size(self.image_width, self.image_height, w, h)

        self.new_image = self.new_image.resize((w, h), Image.ANTIALIAS)

        self.disp_new_image = ImageTk.PhotoImage(self.new_image)
        self.new_img_canvas = tk.Canvas(self.new_image_frame, height=h, width=w, bg="gray", bd=0, highlightthickness=0,
                                        relief='ridge')
        self.new_img_canvas.create_image(0, 0, anchor=tk.NW, image=self.disp_new_image)
        self.new_img_canvas.pack()
