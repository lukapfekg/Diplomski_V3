import tkinter
import tkinter as tk
import os
from os import *
from tkinter import filedialog

from PIL import ImageTk, Image
from tkinterdnd2 import DND_FILES

from gui.util_gui import calculate_size, get_histogram, write_array_to_file
from jpeg.compression import image_compression
from jpeg.decompression import *
from jpeg.dictionary_util import *
from jpeg.image_scaling import upscale

##################################################
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


###################################################

class InitialScreen:

    def __init__(self, root):
        self.filename = None
        self.img = None
        self.drag_and_drop_img = None
        self.root = root
        self.has_image = False

        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(root, height=self.height, width=self.width, bg="#263D42")

        # image frame
        self.frame = tk.Frame(self.canvas, bg="#263D42")
        self.frame.place(relheight=0.8, relwidth=0.8, relx=0.025, rely=0.125)
        self.frame.drop_target_register(DND_FILES)
        self.frame.dnd_bind("<<Drop>>", self.drag_and_drop_image)

        # image canvas
        self.img_canvas_h = self.height * 0.8
        self.img_canvas_w = self.width * 0.8
        self.img_canvas = tk.Canvas(self.frame, height=self.img_canvas_h, width=self.img_canvas_w, bg="#354552", bd=0,
                                    highlightthickness=0,
                                    relief='ridge')

        # image label
        self.image_label = tk.Label(self.img_canvas, text="Drag and drop an image here", justify=tk.CENTER,
                                    width=80, height=1, font=("Roboto", 16, "bold"), bg="#354552", fg="#CABAAD")
        self.image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.img_canvas.pack()

        # button frame
        self.button_frame = tk.Frame(self.canvas, bg="#354552")
        self.button_frame.place(relwidth=0.125, relheight=0.5, relx=0.86, rely=0.25)

        # next canvas button
        button_next = tk.Button(self.button_frame, text="Change window", height=5, width=15, fg="white", bg="#263D42")
        button_next.configure(command=self.change_canvas)
        button_next.pack(side=tkinter.TOP, pady=10)

        # text frame
        self.text_frame = tk.Frame(self.canvas, bg="#263D42")
        self.text_frame.place(relheight=0.08, relwidth=0.8, relx=0.025, rely=0.025)

        # text label
        self.display_text = tk.StringVar()
        self.text_label = tk.Label(self.text_frame, textvariable=self.display_text, justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 12, "bold"), bg="#354552", fg="white")
        self.text_label.pack(side=tk.LEFT, padx=10)

        # add image button
        button_add_image = tk.Button(self.text_frame, text="Add image", height=2, width=30, fg="white", bg="#263D42")
        button_add_image.configure(command=self.search_image)
        button_add_image.pack(side=tkinter.RIGHT, padx=20)

        self.canvas.pack()

    def change_canvas(self):
        print('uslooo')
        if self.has_image:
            self.canvas.destroy()
            SecondScreen(self.root, self.filename)

    def search_image(self):
        filename = filedialog.askopenfilename(initialdir="Examples/", title="Select file",
                                              filetypes=(("images", "*.jpg"), ("images", "*.png")))
        self.filename = filename
        self.display_text.set(filename)
        print('filename: ', filename)

        if filename != '':
            self.display_image(filename)
            self.has_image = True

    def display_image(self, filename):
        self.img_canvas.destroy()

        self.img = Image.open(filename)
        w, h = self.img.size
        w, h = calculate_size(self.img_canvas_w, self.img_canvas_h, w, h)

        self.img = self.img.resize((w, h), Image.ANTIALIAS)
        # self.img.thumbnail((w, h), Image.ANTIALIAS)
        # self.img.save('miner_resized.jpg')

        self.drag_and_drop_img = ImageTk.PhotoImage(self.img)
        self.img_canvas = tk.Canvas(self.frame, height=h, width=w, bg="gray", bd=0, highlightthickness=0,
                                    relief='ridge')
        self.img_canvas.create_image(0, 0, anchor=tk.NW, image=self.drag_and_drop_img)
        self.img_canvas.pack()
        threading.Thread(target=self.compress_image, args=[filename]).start()

    def compress_image(self, filename):
        # load image
        image = Image.open(filename)
        image = np.array(image)
        h, w = image.shape[0], image.shape[1]

        if len(image.shape) == 3:
            image = Image.open(filename).convert('YCbCr')
            image = np.array(image)

        # start compression
        start = time.time()
        out = image_compression(image)
        end = time.time()
        diff_compression = end - start
        print("compression time", diff_compression)

        # star decompression thread
        threading.Thread(target=self.decompress_image, args=[out, h, w]).start()

    def decompress_image(self, bit_array, h, w):
        start = time.time()

        if len(bit_array) == 3:
            y = decompress(bit_array[0], False)
            cr = decompress(bit_array[1], False)
            cb = decompress(bit_array[2], False)

            y = y[:h, :w]

            cr = upscale(cr, 2)
            cr = cr[:h, :w]

            cb = upscale(cb, 2)
            cb = cb[:h, :w]

            image = np.zeros((h, w, 3)).astype(np.uint8)
            image[:, :, 0] = y.astype(np.uint8)
            image[:, :, 1] = cr.astype(np.uint8)
            image[:, :, 2] = cb.astype(np.uint8)

            image = Image.fromarray(image, mode='YCbCr')
            print(image.mode)
            image = image.convert('RGB')

            image.save("temp/decompressed.jpg")
            print("decompression done!")

        else:
            y = decompress(bit_array, False)
            y = y[:h, :w]

            y = color.gray2rgb(y)
            imsave("temp/decompressed.jpg", y)

        end = time.time()
        diff_decompression = end - start
        print("decompression time", diff_decompression)

    def drag_and_drop_image(self, event):
        filename = event.data
        self.filename = filename
        if filename is not None and (
                ".jpg" in filename or ".png" in filename or '.tif' in filename or '.bmp' in filename):
            self.display_text.set(filename)
            self.display_image(filename)

            self.has_image = True


class SecondScreen:
    def __init__(self, root, filename):
        self.new_image = None
        self.disp_old_image = None
        self.old_image = None
        self.root = root
        self.filename = filename
        self.image_height = 640
        self.image_width = 540
        self.histo_old = None
        self.histo_new = None
        self.canvas = tk.Canvas(root, height=900, width=1500, bg="#263D42")

        # old image frame
        self.frame = tk.Frame(self.canvas, bg="#263D42")
        self.frame.place(relheight=0.8, relwidth=0.45, relx=0.025, rely=0.05)

        # new image frame
        self.new_image_frame = tk.Frame(self.canvas, bg="#263D42")
        self.new_image_frame.place(relheight=0.8, relwidth=0.45, relx=0.525, rely=0.05)

        # button_frame
        self.button_frame = tk.Frame(self.canvas, bg="#354552")
        self.button_frame.place(relheight=0.1, relwidth=0.95, relx=0.025, rely=0.875)

        # image canvases
        self.old_img_canvas = tk.Canvas(self.frame, height=self.image_height, width=self.image_width, bg="#354552",
                                        bd=0,
                                        highlightthickness=0,
                                        relief='ridge')
        self.old_img_canvas.pack()
        self.new_img_canvas = tk.Canvas(self.frame, height=self.image_height, width=self.image_width, bg="#354552",
                                        bd=0,
                                        highlightthickness=0,
                                        relief='ridge')
        self.new_img_canvas.pack()

        # new compression button
        button = tk.Button(self.button_frame, text="Return", padx=10, pady=10, fg="white", bg="#263D42")
        button.configure(command=self.change_canvas, height=2)
        button.pack(side=tk.LEFT)

        # histo button
        histo_button = tk.Button(self.button_frame, text="Info", padx=10, pady=10, fg="white", bg="#263D42")
        histo_button.configure(command=self.to_histo, height=2)
        histo_button.pack(pady=11, padx=20)

        self.display_images()

        self.canvas.pack()

    def change_canvas(self):
        print('uslooo')
        self.canvas.destroy()
        # os.remove("temp/compressed.txt")
        os.remove("temp/decompressed.jpg")
        InitialScreen(self.root)

    def to_histo(self):
        self.canvas.destroy()
        HistoScreen(self.root, self.filename, self.histo_old, self.histo_new)

    def display_images(self):
        self.old_img_canvas.destroy()

        self.old_image = Image.open(self.filename)
        w, h = self.old_image.size
        w, h = calculate_size(self.image_width, self.image_height, w, h)

        image = np.array(self.old_image)
        threading.Thread(target=self.get_histo, args=[image, True]).start()

        # self.old_image.thumbnail((w, h), Image.ANTIALIAS)

        self.old_image = self.old_image.resize((w, h), Image.ANTIALIAS)

        self.disp_old_image = ImageTk.PhotoImage(self.old_image)
        self.old_img_canvas = tk.Canvas(self.frame, height=h, width=w, bg="gray", bd=0, highlightthickness=0,
                                        relief='ridge')
        self.old_img_canvas.create_image(0, 0, anchor=tk.NW, image=self.disp_old_image)
        self.old_img_canvas.pack()
        threading.Thread(target=self.display_new_image).start()

    def display_new_image(self):
        self.new_img_canvas.destroy()

        while 1:
            if path.exists("temp/decompressed.jpg"):
                break

        self.new_image = Image.open("temp/decompressed.jpg")
        w, h = self.new_image.size
        w, h = calculate_size(self.image_width, self.image_height, w, h)

        image = np.array(self.new_image)
        threading.Thread(target=self.get_histo, args=[image, False]).start()

        # self.new_image.thumbnail((w, h), Image.ANTIALIAS)
        self.new_image = self.new_image.resize((w, h), Image.ANTIALIAS)

        self.disp_new_image = ImageTk.PhotoImage(self.new_image)
        self.new_img_canvas = tk.Canvas(self.new_image_frame, height=h, width=w, bg="gray", bd=0, highlightthickness=0,
                                        relief='ridge')
        self.new_img_canvas.create_image(0, 0, anchor=tk.NW, image=self.disp_new_image)
        self.new_img_canvas.pack()

    def get_histo(self, image, old=True):
        keys, values = get_histogram(image.flatten())
        histo = list(np.zeros(256).astype(int))

        for k, i in enumerate(keys):
            histo[k] = values[i]

        if old:
            self.histo_old = histo
        else:
            self.histo_new = histo


class HistoScreen:
    def __init__(self, root, filename, histo_before, histo_after):
        self.new_image = None
        self.disp_old_image = None
        self.old_image = None
        self.root = root
        self.filename = filename
        self.image_height = 640
        self.image_width = 540
        self.histo_before = histo_before
        self.histo_after = histo_after
        self.canvas = tk.Canvas(root, height=900, width=1500, bg="#263D42")

        # old image frame
        self.frame = tk.Frame(self.canvas, bg="#354552")
        self.frame.place(relheight=0.8, relwidth=0.45, relx=0.025, rely=0.05)

        # new image frame
        self.frame2 = tk.Frame(self.canvas, bg="#263D42")
        self.frame2.place(relheight=0.8, relwidth=0.45, relx=0.525, rely=0.05)

        # button_frame
        self.button_frame = tk.Frame(self.canvas, bg="#354552")
        self.button_frame.place(relheight=0.1, relwidth=0.95, relx=0.025, rely=0.875)

        # button to second screen
        button = tk.Button(self.button_frame, text="Return", padx=10, pady=10, fg="white", bg="#263D42")
        button.configure(command=self.to_second_screen, height=2)
        button.pack(pady=11)

        self.plot_histo(self.frame, self.histo_before)
        self.plot_histo(self.frame2, self.histo_after)

        self.canvas.pack()

    def to_second_screen(self):
        self.canvas.destroy()
        SecondScreen(self.root, self.filename)

    def plot_histo(self, frame, histo):
        # fig
        fig = Figure(figsize=(8, 8), dpi=100)

        bins = [i for i in range(256)]

        plot1 = fig.add_subplot(111)
        plot1.bar(bins, histo)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()

        canvas.get_tk_widget().pack()
