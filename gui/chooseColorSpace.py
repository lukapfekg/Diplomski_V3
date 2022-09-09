import tkinter
import tkinter as tk
import os
from multiprocessing import Pool
from os import *
from tkinter import filedialog

import numpy as np
from PIL import ImageTk, Image
from tkinterdnd2 import DND_FILES

# from gui.chooseColorSpace import ChooseColorSpace
from gui.util_gui import calculate_size, get_histogram, write_array_to_file, convert_bits
from jpeg.compression import image_compression
from jpeg.decompression import *
from jpeg.dictionary_util import *
from jpeg.image_scaling import upscale

from gui.util_gui import calculate_size


class ChooseColorSpace:

    def __init__(self, root, filename):
        self.drag_and_drop_img = None
        self.size_old = None
        self.filename = filename
        self.img = None
        self.root = root

        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg="#263D42")

        # print("filename: ", self.filename)

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
        self.clicked.set("Choose color space")

        self.drop = tk.OptionMenu(self.button_frame, self.clicked, *self.options)
        self.drop.config(width=20, font=("Roboto", 16, "bold"), foreground="#FFFFFF", background="#263D42")
        self.drop.pack()

        button_dropdown = tk.Button(self.button_frame, text="JPEG", height=5, width=25, fg="white", bg="#263D42")
        button_dropdown.configure(command=self.accept_color_space)
        button_dropdown.pack(side=tk.BOTTOM, pady=10)

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
            if s == 'RGB':
                image = Image.open(self.filename)
                image = np.array(image)

            else:
                image = Image.open(self.filename).convert('YCbCr')
                image = np.array(image)
                y = image[:, :, 0]
                cb = image[:, :, 1]
                cr = image[:, :, 2]

                if '420' in s:
                    cb = blockify(cb)
                    cr = blockify(cr)


# TODO: change name of a method
def blockify(arr):
    h, w = arr.shape

    out = np.zeros((int(np.ceil(h / 2)), int(np.ceil(w / 2))))
    h, w = out.shape

    for i in range(h):
        for j in range(w):
            out[i, j] = arr[i * 2, j * 2]

    return out
