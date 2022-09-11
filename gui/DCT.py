import tkinter
import tkinter as tk
import os
from multiprocessing import Pool
from os import *
from tkinter import filedialog

import numpy as np
from PIL import ImageTk, Image
from tkinterdnd2 import DND_FILES

from gui.predictive_encoding import PredictiveEncoding
from gui.util_gui import calculate_size, get_histogram, write_array_to_file, convert_bits
from jpeg.compression import image_compression
from jpeg.decompression import *
from jpeg.dictionary_util import *
from jpeg.image_scaling import upscale

from gui.util_gui import calculate_size


class ChooseDCT:

    def __init__(self, root, color_space, img1, img2, img3, out):
        self.show_image2 = None
        self.show_image1 = None
        self.root = root
        self.color_space = color_space
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3
        self.out = out

        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg="#263D42")

        print(self.out)

        if color_space == 'RGB' or color_space == 'YCbCr444':
            # image frame
            self.frame1 = tk.Frame(self.canvas, bg="#263D42")
            self.frame1.place(relheight=0.6, relwidth=0.25, relx=0.025, rely=0.2)
            self.frame2 = tk.Frame(self.canvas, bg="#263D42")
            self.frame2.place(relheight=0.6, relwidth=0.25, relx=0.28, rely=0.2)
            self.frame3 = tk.Frame(self.canvas, bg="#263D42")
            self.frame3.place(relheight=0.6, relwidth=0.25, relx=0.535, rely=0.2)

            # canvas width and height
            self.img_canvas1_h = int(self.height * 0.6)
            self.img_canvas1_w = int(self.width * 0.2)
            self.img_canvas2_h = int(self.height * 0.6)
            self.img_canvas2_w = int(self.width * 0.2)

            # image component labels
            first = "R" if color_space == 'RGB' else "Y"
            second = "G" if color_space == 'RGB' else "Cb"
            third = "B" if color_space == 'RGB' else "Cr"

            self.label_frame1 = tk.Frame(self.canvas, bg="#263D42")
            self.label_frame1.place(relheight=0.028, relwidth=0.25, relx=0.025, rely=0.17)
            self.label_frame2 = tk.Frame(self.canvas, bg="#263D42")
            self.label_frame2.place(relheight=0.028, relwidth=0.25, relx=0.28, rely=0.17)
            self.label_frame3 = tk.Frame(self.canvas, bg="#263D42")
            self.label_frame3.place(relheight=0.028, relwidth=0.25, relx=0.535, rely=0.17)
            self.label1 = tk.Label(self.label_frame1, text=first, justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 12, "bold"), bg="#263D42", fg="white")
            self.label1.pack()
            self.label2 = tk.Label(self.label_frame2, text=second, justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 12, "bold"), bg="#263D42", fg="white")
            self.label2.pack()
            self.label3 = tk.Label(self.label_frame3, text=third, justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 12, "bold"), bg="#263D42", fg="white")
            self.label3.pack()

            # drop-down frame
            self.button_frame = tk.Frame(self.canvas, bg="#354552")
            self.button_frame.place(relwidth=0.2, relheight=0.2, relx=0.79, rely=0.3)

            # drop down menu
            self.options1 = ["DCT", "No DCT"]
            self.clicked1 = tk.StringVar()
            self.clicked1.set("Choose transformation encoding")

            self.drop = tk.OptionMenu(self.button_frame, self.clicked1, *self.options1)
            self.drop.config(width=30, font=("Roboto", 12, "bold"), foreground="#FFFFFF", background="#263D42")
            self.drop.pack()

            self.options2 = ["4x4", "8x8", "16x16"]
            self.clicked2 = tk.StringVar()
            self.clicked2.set("Choose block size")

            self.drop2 = tk.OptionMenu(self.button_frame, self.clicked2, *self.options2)
            self.drop2.config(width=30, font=("Roboto", 12, "bold"), foreground="#FFFFFF", background="#263D42")
            self.drop2.pack(pady=20)

            button_dropdown = tk.Button(self.button_frame, text="Choose", height=5, width=25, fg="white", bg="#263D42")
            button_dropdown.configure(command=self.accept_DCT)
            button_dropdown.pack(side=tk.BOTTOM, pady=10)

            # TODO: add horizontal aligning
        else:
            # image frame
            self.frame1 = tk.Frame(self.canvas, bg="#263D42")
            self.frame1.place(relheight=0.8, relwidth=0.4, relx=0.025, rely=0.1)
            self.frame2 = tk.Frame(self.canvas, bg="#263D42")
            self.frame2.place(relheight=0.375, relwidth=0.15, relx=0.475, rely=0.1)
            self.frame3 = tk.Frame(self.canvas, bg="#263D42")
            self.frame3.place(relheight=0.375, relwidth=0.15, relx=0.475, rely=0.525)

            self.img_canvas1_h = int(self.height * 0.8)
            self.img_canvas1_w = int(self.width * 0.4)
            self.img_canvas2_h = int(self.height * 0.375)
            self.img_canvas2_w = int(self.width * 0.15)

        # image canvases
        self.img_canvas1 = tk.Canvas(self.frame1, height=self.img_canvas1_h, width=self.img_canvas1_w, bg="#263D42",
                                     bd=0,
                                     highlightthickness=0,
                                     relief='ridge')
        self.img_canvas1.pack()
        self.img_canvas2 = tk.Canvas(self.frame2, height=self.img_canvas2_h, width=self.img_canvas2_w, bg="#263D42",
                                     bd=0,
                                     highlightthickness=0,
                                     relief='ridge')
        self.img_canvas2.pack()
        self.img_canvas3 = tk.Canvas(self.frame3, height=self.img_canvas2_h, width=self.img_canvas2_w, bg="#263D42",
                                     bd=0,
                                     highlightthickness=0,
                                     relief='ridge')
        self.img_canvas3.pack()

        button_JPEG = tk.Button(self.frame1, text="JPEG", height=5, width=15, fg="white", bg="#263D42")
        button_JPEG.configure(command=self.show_images)
        # button_JPEG.pack(side=tkinter.TOP, pady=10)

        self.show_images()

        self.canvas.pack()

    def show_images(self):
        self.img_canvas1.destroy()
        self.img_canvas2.destroy()
        self.img_canvas3.destroy()

        image1 = Image.fromarray(self.img1).convert('L')
        image2 = Image.fromarray(self.img2).convert('L')
        image3 = Image.fromarray(self.img3).convert('L')

        w, h = image1.size
        print(self.img_canvas1_w, self.img_canvas1_h)
        print(w, h)
        w, h = calculate_size(self.img_canvas1_w, self.img_canvas1_h, w, h)
        print(w, h)
        image1 = image1.resize((w, h), Image.ANTIALIAS)
        self.show_image1 = ImageTk.PhotoImage(image1)
        self.img_canvas1 = tk.Canvas(self.frame1, height=h, width=w, bg="gray", bd=0, highlightthickness=0,
                                     relief='ridge')
        self.img_canvas1.create_image(0, 0, anchor=tk.NW, image=self.show_image1)
        self.img_canvas1.pack()

        w, h = image2.size
        w, h = calculate_size(self.img_canvas2_w, self.img_canvas2_h, w, h)
        image2 = image2.resize((w, h), Image.ANTIALIAS)
        self.show_image2 = ImageTk.PhotoImage(image2)
        self.img_canvas2 = tk.Canvas(self.frame2, height=h, width=w, bg="gray", bd=0, highlightthickness=0,
                                     relief='ridge')
        self.img_canvas2.create_image(0, 0, anchor=tk.NW, image=self.show_image2)
        self.img_canvas2.pack()

        w, h = image3.size
        w, h = calculate_size(self.img_canvas2_w, self.img_canvas2_h, w, h)
        image3 = image3.resize((w, h), Image.ANTIALIAS)
        self.show_image3 = ImageTk.PhotoImage(image3)
        self.img_canvas3 = tk.Canvas(self.frame3, height=h, width=w, bg="gray", bd=0, highlightthickness=0,
                                     relief='ridge')
        self.img_canvas3.create_image(0, 0, anchor=tk.NW, image=self.show_image3)
        self.img_canvas3.pack()

    def accept_DCT(self):

        if self.clicked1.get() in self.options1:
            print(self.clicked1.get())

            if self.clicked1.get() == "DCT":
                if self.clicked2.get() in self.options2:
                    block_size = 4 if '4' in self.clicked2.get() else (8 if '8' in self.clicked2.get() else 16)
                    self.out = self.out + '4;' if '4' in self.clicked2.get() else (
                        '8;' if '8' in self.clicked2.get() else '6;')


                    print(self.img1[:8, :8])
                    self.img1 -= 128
                    dct_image1 = calc_dct(self.img1, block_size)
                    self.img2 -= 128
                    dct_image2 = calc_dct(self.img3, block_size)
                    self.img3 -= 128
                    dct_image3 = calc_dct(self.img3, block_size)

                    print(self.img1[:8, :8])

                    self.canvas.destroy()
                    PredictiveEncoding(self.root, dct_image1, dct_image2, dct_image3, self.out)

            else:
                self.out = self.out + '0;'
                print(self.out)

        else:
            print('ERROR')
