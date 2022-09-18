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

# from gui.chooseColorSpace import ChooseColorSpace
from gui.DCT import ChooseDCT
from gui.util_gui import calculate_size, get_histogram, write_array_to_file, convert_bits
from jpeg.compression import image_compression
from jpeg.decompression import *
from jpeg.dictionary_util import *
from jpeg.image_scaling import upscale

from gui.util_gui import calculate_size
from util.bilinear_trasformation import bilinear_interpolation


class ChooseColorSpace:

    def __init__(self, root, filename, out):
        self.entropy = None
        self.drag_and_drop_img = None
        self.size_old = None
        self.filename = filename
        self.img = None
        self.root = root
        self.out = out

        self.calc_entropy()

        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg="#263D42")


        # image frame
        self.frame = tk.Frame(self.canvas, bg="#263D42")
        self.frame.place(relheight=0.8, relwidth=0.6, relx=0.025, rely=0.1)

        # image canvas
        self.img_canvas_h = self.height * 0.8
        self.img_canvas_w = self.width * 0.6
        self.img_canvas = tk.Canvas(self.frame, height=self.img_canvas_h, width=self.img_canvas_w, bg="#263D42", bd=0,
                                    highlightthickness=0,
                                    relief='ridge')
        self.img_canvas.pack()

        # button frame
        self.button_frame = tk.Frame(self.canvas, bg="#263D42")
        self.button_frame.place(relwidth=0.3, relheight=0.2, relx=0.67, rely=0.3)

        # next canvas button
        button_JPEG = tk.Button(self.button_frame, text="JPEG", height=5, width=15, fg="white", bg="#263D42")
        button_JPEG.configure(command=self.display_image)
        # button_JPEG.pack(side=tkinter.TOP, pady=10)

        # drop down menu
        self.options = ["RGB", "YCbCr444", "YCbCr420"]
        self.clicked = tk.StringVar()
        self.clicked.set("YCbCr444")
        # self.clicked.set("Choose color space")

        self.drop = tk.OptionMenu(self.button_frame, self.clicked, *self.options)
        self.drop.config(width=20, font=("Roboto", 16, "bold"), foreground="#FFFFFF", background="#263D42")
        self.drop.pack()

        button_dropdown = tk.Button(self.button_frame, text="JPEG", height=5, width=25, fg="white", bg="#263D42")
        button_dropdown.configure(command=self.accept_color_space)
        button_dropdown.pack(side=tk.BOTTOM, pady=10)

        # entropy frame
        self.entropy_frame = tk.Frame(self.canvas, bg="#354552")
        self.entropy_frame.place(relwidth=0.3, relheight=0.175, relx=0.67, rely=0.55)

        # entropy label
        self.entropy_label = tk.Label(self.entropy_frame, text='Entropy', justify=tk.CENTER,
                                      width=80, height=1, font=("Roboto", 16, "bold"), bg="#354552", fg="white")
        self.entropy_label.pack(side=tk.TOP, pady=20)
        self.entropy_label1 = tk.Label(self.entropy_frame, text=str(self.entropy), justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 16, "bold"), bg="#354552", fg="white")
        self.entropy_label1.pack(side=tk.TOP, pady=20)

        self.display_image()
        self.canvas.pack()

    def display_image(self):
        self.img_canvas.destroy()

        self.img = Image.open(self.filename)
        w, h = self.img.size
        w, h = calculate_size(self.img_canvas_w, self.img_canvas_h, w, h)

        self.img = self.img.resize((w, h), Image.ANTIALIAS)

        self.drag_and_drop_img = ImageTk.PhotoImage(self.img)
        self.img_canvas = tk.Canvas(self.frame, height=h, width=w, bg="gray", bd=0, highlightthickness=0,
                                    relief='ridge')
        self.img_canvas.create_image(0, 0, anchor=tk.NW, image=self.drag_and_drop_img)
        self.img_canvas.pack()


    def accept_color_space(self):
        s = self.clicked.get()

        if s in self.options:
            self.canvas.destroy()

            if s == 'RGB':
                image = Image.open(self.filename)
                image = np.array(image)
                r = image[:, :, 0]
                g = image[:, :, 1]
                b = image[:, :, 2]
                self.out = self.out + 'R;'
                ChooseDCT(self.root, s, r, g, b, self.out, self.filename)

            else:
                image = Image.open(self.filename).convert('YCbCr')
                image = np.array(image)
                y = image[:, :, 0]
                cb = image[:, :, 1]
                cr = image[:, :, 2]
                if '420' in s:
                    cb = blockify(cb)
                    cr = blockify(cr)

                self.out = self.out + ('4;' if '444' in s else '2;')
                ChooseDCT(self.root, s, y, cb, cr, self.out, self.filename)

    def calc_entropy(self):
        image = Image.open(self.filename)
        image = np.array(image)

        self.entropy = skimage.measure.shannon_entropy(image)
        print("entropy1:", self.entropy)


# TODO: change name of a method
def blockify(arr):
    h, w = arr.shape

    out = np.zeros((int(np.ceil(h / 2)), int(np.ceil(w / 2))))
    h, w = out.shape

    for i in range(h):
        for j in range(w):
            out[i, j] = arr[i * 2, j * 2]

    return out
