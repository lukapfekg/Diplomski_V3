import builtins
import tkinter as tk

import skimage.metrics
from bitarray import bitarray

from gui.ResultWindow import ResultWindow
from jpeg.decompression import *
from jpeg.dictionary_util import *
from util.bilinear_trasformation import bilinear_interpolation
from util.dictionary_util_modular import decompress_dict_modular


class Decompression:

    def __init__(self, root, image, out, filename):
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
        self.compressed_size = len(image)
        self.out = out
        self.filename = filename

        bin_file = builtins.open("compressed_image_bin.dat", 'w')
        bin_file.write(self.image_bin)
        bin_file.close()

        # canvas
        self.height = 900
        self.width = 1500
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg="#263D42")

        # info frame
        self.frame = tk.Frame(self.canvas, bg="#354552")
        self.frame.place(relheight=0.72, relwidth=0.6, relx=0.025, rely=0.12)

        self.read_file()
        print("image bin len: ", len(self.image_bin))

        # labels
        self.img_height = "Height: " + str(self.image_height)
        self.label1 = tk.Label(self.frame, text=self.img_height, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label1.pack(side=tk.TOP, pady=15)

        self.img_width = "Width: " + str(self.image_width)
        self.label2 = tk.Label(self.frame, text=self.img_width, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label2.pack(side=tk.TOP, pady=15)

        self.color_space = "Color space: " + self.image_color_space
        self.label3 = tk.Label(self.frame, text=self.color_space, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label3.pack(side=tk.TOP, pady=15)

        self.dct = 'Has DCT' if self.has_dct else 'No DCT'
        self.dct = "DCT: " + self.dct
        self.label4 = tk.Label(self.frame, text=self.dct, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label4.pack(side=tk.TOP, pady=15)

        if self.has_dct:
            self.dct = "DCT: " + self.dct
            self.label5 = tk.Label(self.frame, text='Block size: ' + str(self.block_size) + 'x' + str(self.block_size),
                                   justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
            self.label5.pack(side=tk.TOP, pady=15)

        self.label6 = tk.Label(self.frame, text='Quantization: ' + str(self.quant), justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label6.pack(side=tk.TOP, pady=15)

        if self.quant_val != 0:
            self.label7 = tk.Label(self.frame, text='Quantization value: ' + str(self.quant_val), justify=tk.CENTER,
                                   width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
            self.label7.pack(side=tk.TOP, pady=15)

        pred = 'No' if not self.predictive else 'Yes' if self.dct else 'Vertical' if self.vertical else 'Horizontal'
        self.label9 = tk.Label(self.frame, text='Predictive encoding: ' + pred, justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label9.pack(side=tk.TOP, pady=15)

        self.label8 = tk.Label(self.frame, text='Encoding: ' + str(self.encoding), justify=tk.CENTER,
                               width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label8.pack(side=tk.TOP, pady=15)

        compression_rate = int(self.image_height) * int(self.image_width) * 3 * 8 / self.compressed_size
        self.label10 = tk.Label(self.frame, text='Compression rate: ' + str(compression_rate), justify=tk.CENTER,
                                width=80, height=1, font=("Roboto", 22, "bold"), bg="#354552", fg="white")
        self.label10.pack(side=tk.TOP, pady=15)

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
            if self.has_dct:
                zigzag = self.from_bit_array_to_zigzag(self.image)
                zigzag1, zigzag2, zigzag3 = self.get_images(zigzag)
                # recreate dct image
                # inverse zig-zag

                inverse_zigzag1 = inverse_zigzag_optimized(zigzag1, self.block_size)
                inverse_zigzag2 = inverse_zigzag_optimized(zigzag2, self.block_size)
                inverse_zigzag3 = inverse_zigzag_optimized(zigzag3, self.block_size)

                if self.predictive:
                    # inverse predictive
                    curr = 0
                    for i in range(len(inverse_zigzag1)):
                        if i != 0:
                            inverse_zigzag1[i][0, 0] = curr + inverse_zigzag1[i][0, 0]

                        curr = inverse_zigzag1[i][0, 0]

                    for i in range(len(inverse_zigzag2)):
                        if i != 0:
                            inverse_zigzag2[i][0, 0] = curr + inverse_zigzag2[i][0, 0]

                        curr = inverse_zigzag2[i][0, 0]

                    for i in range(len(inverse_zigzag3)):
                        if i != 0:
                            inverse_zigzag3[i][0, 0] = curr + inverse_zigzag3[i][0, 0]

                        curr = inverse_zigzag3[i][0, 0]

                if self.quant:
                    # inverse quantization
                    inverse_zigzag1 = self.inverse_quantization(inverse_zigzag1)
                    inverse_zigzag2 = self.inverse_quantization(inverse_zigzag2)
                    inverse_zigzag3 = self.inverse_quantization(inverse_zigzag3)

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
                out_image = image.copy()

                original = Image.open(self.filename).convert(
                    'YCbCr') if 'Y' in self.image_color_space else Image.open(self.filename)
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

                self.canvas.destroy()
                ResultWindow(self.root, self.filename, out_image, self.color_space,
                             int(self.height) * int(self.width) * 3 * 8, self.compressed_size)

            else:
                start = time.time()
                rle = self.get_rle_no_dct()
                end = time.time()
                print(end - start)

                start = time.time()
                image1, image2, image3 = self.get_images_no_dct(rle)
                end = time.time()
                print(end - start)

                if self.predictive:
                    image1 = self.inverse_predictive(image1)
                    image2 = self.inverse_predictive(image2)
                    image3 = self.inverse_predictive(image3)

                if self.quant:
                    image1 = np.multiply(image1, self.quant_val)
                    image2 = np.multiply(image2, self.quant_val)
                    image3 = np.multiply(image3, self.quant_val)

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

                out_image = image.copy()

                original = Image.open(self.filename).convert(
                    'YCbCr') if 'Y' in self.image_color_space else Image.open(self.filename)
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

                image.save("decompressed_no_dct.jpg")

                self.canvas.destroy()
                ResultWindow(self.root, self.filename, out_image, self.color_space,
                             int(self.height) * int(self.width) * 3 * 8, self.compressed_size)

        elif 'Entropy' in self.encoding:
            image1, image2, image3 = self.from_bit_array()

            if self.has_dct:
                if self.predictive:
                    image1 = self.inverse_predictive_dct(image1)
                    image2 = self.inverse_predictive_dct(image2)
                    image3 = self.inverse_predictive_dct(image3)

                if self.quant:
                    image1 = self.inverse_quantization(image1, False)
                    image2 = self.inverse_quantization(image2, False)
                    image3 = self.inverse_quantization(image3, False)

                image1 = self.inverse_dct(image1, True, False)
                image2 = self.inverse_dct(image2, False, False)
                image3 = self.inverse_dct(image3, False, False)

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

                out_image = image.copy()

                original = Image.open(self.filename).convert(
                    'YCbCr') if 'Y' in self.image_color_space else Image.open(self.filename)
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

                image.save("decompressed_no_dct.jpg")

                self.canvas.destroy()
                ResultWindow(self.root, self.filename, out_image, self.color_space,
                             int(self.height) * int(self.width) * 3 * 8, self.compressed_size)

            else:
                image1, image2, image3 = self.from_bit_array()

                if self.predictive:
                    image1 = self.inverse_predictive(image1)
                    image2 = self.inverse_predictive(image2)
                    image3 = self.inverse_predictive(image3)

                if self.quant:
                    image1 = np.multiply(image1, self.quant_val)
                    image2 = np.multiply(image2, self.quant_val)
                    image3 = np.multiply(image3, self.quant_val)

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

                out_image = image.copy()

                original = Image.open(self.filename).convert(
                    'YCbCr') if 'Y' in self.image_color_space else Image.open(self.filename)
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

                image.save("decompressed_no_dct.jpg")

                self.canvas.destroy()
                ResultWindow(self.root, self.filename, out_image, self.color_space,
                             int(self.height) * int(self.width) * 3 * 8, self.compressed_size)

        self.decompressed = None

    def from_bit_array_to_zigzag(self, bit_array):
        dec = bitarray(self.image).decode(self.dictionary)

        out = []
        out_array = []
        for elem in dec:

            if ',' in elem:
                elem = elem[1:-1]
                l, r = elem.split(',')

                out_temp = ['0'] * int(l)
                out_temp.append(r)

                out += out_temp

                if len(out) == self.block_size ** 2:
                    out_array.append(out)
                    out = []

            elif elem == 'E':
                elem = ['0'] * (self.block_size ** 2 - len(out))

                out += elem
                out_array.append(out)
                out = []

            else:
                out.append(elem)

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

    def inverse_quantization(self, array, RLE=True):
        quant = QUANTIZATION_MATRIX if self.block_size == 8 else (
            QUANTIZATION_MATRIX_16 if self.block_size == 16 else QUANTIZATION_MATRIX_4)

        out_array = []

        if RLE:
            for elem in array:
                out_array.append(np.multiply(elem, quant))

        else:
            h, w = array.shape

            h = int(h // self.block_size)
            w = int(w // self.block_size)

            for i in range(h):
                for j in range(w):
                    temp = array[i * self.block_size: i * self.block_size + self.block_size,
                           j * self.block_size:j * self.block_size + self.block_size]
                    mul = np.multiply(
                        array[i * self.block_size: i * self.block_size + self.block_size,
                        j * self.block_size:j * self.block_size + self.block_size],
                        quant
                    )

                    array[i * self.block_size: i * self.block_size + self.block_size,
                    j * self.block_size:j * self.block_size + self.block_size] = np.multiply(temp, quant)

            out_array = array.copy()

        return out_array

    def inverse_dct(self, array, first=True, RLE=True):
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
                tek = array[k] \
                    if RLE else \
                    array[i * self.block_size:i * self.block_size + self.block_size,
                    j * self.block_size:j * self.block_size + self.block_size]

                tek = fftpack.idct(fftpack.idct(tek.T, norm='ortho').T, norm='ortho').astype(int)
                tek += 128
                tek[tek < 0] = 0
                tek[tek > 255] = 255

                out_image[i * self.block_size:i * self.block_size + self.block_size,
                j * self.block_size:j * self.block_size + self.block_size] = tek

                k += 1

        return out_image

    def get_rle_no_dct(self):
        dec = bitarray(self.image).decode(self.dictionary)

        out_array = []

        for elem in dec:
            temp = elem[1:-1]
            l, r = temp.split(',')

            out_temp = [int(r)] * int(l)
            out_array += out_temp

        print('out_array_len optimized: ', len(out_array))

        return out_array

    def get_images_no_dct(self, image_array):
        h = int(self.image_height)
        w = int(self.image_width)

        image_array = np.array(image_array)

        image1 = image_array[:h * w]
        image_array = image_array[h * w:]
        image1 = np.reshape(image1, (h, w), order='F' if self.vertical else 'C')

        if '420' in self.color_space:
            h = int(h / 2)
            w = int(w / 2)

        image2 = image_array[:h * w]
        image_array = image_array[h * w:]
        image3 = image_array[:h * w]
        image_array = image_array[h * w:]

        image2 = np.reshape(image2, (h, w), order='F' if self.vertical else 'C')
        image3 = np.reshape(image3, (h, w), order='F' if self.vertical else 'C')

        return image1, image2, image3

    def inverse_predictive(self, image):
        h, w = image.shape
        curr = 0

        image = list(np.reshape(image, h * w, order='F' if self.vertical else 'C'))

        for i in range(len(image)):
            if i == 0:
                curr = image[0]
                continue

            image[i] = curr + image[i]
            curr = image[i]

        image = np.reshape(image, (h, w), order='F' if self.vertical else 'C')

        return image

    def from_bit_array(self):
        dec = bitarray(self.image).decode(self.dictionary)

        h = int(self.image_height)
        w = int(self.image_width)
        if self.has_dct:
            h += 0 if h % self.block_size == 0 else self.block_size - h % self.block_size
            w += 0 if w % self.block_size == 0 else self.block_size - w % self.block_size

        image1 = np.reshape(dec[:h * w], (h, w), order='F' if self.vertical else 'C')
        dec = dec[h * w:]

        if '0' in self.color_space:
            h = int(np.ceil(int(self.image_height) / 2))
            w = int(np.ceil(int(self.image_width) / 2))

            if self.block_size != 0:
                h += 0 if h % self.block_size == 0 else self.block_size - h % self.block_size
                w += 0 if w % self.block_size == 0 else self.block_size - w % self.block_size

        image2 = np.reshape(dec[:h * w], (h, w), order='F' if self.vertical else 'C')
        dec = dec[h * w:]
        image3 = np.reshape(dec[:h * w], (h, w), order='F' if self.vertical else 'C')
        dec = dec[h * w:]

        print(dec[:20])
        print(image1[:8, :8])
        print('type', type(image1[0, 0]))

        return image1.astype(int), image2.astype(int), image3.astype(int)

    def inverse_predictive_dct(self, image):
        h, w = image.shape

        h = int(h // self.block_size)
        w = int(w // self.block_size)

        prev = 0
        for i in range(h):
            for j in range(w):
                if i == 0 and j == 0:
                    prev = image[i, j]
                    continue

                image[i * self.block_size, j * self.block_size] = prev + image[i * self.block_size, j * self.block_size]
                prev = image[i * self.block_size, j * self.block_size]

        return image


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

    return out_array, bit_array


def get_dictionary(bit_array):
    curr = ''
    out_array = ''

    ba = bitarray(bit_array)
    pos = ba.tobytes().find('}'.encode('utf-8'))

    arr = bit_array[:(pos + 1) * 8]
    bit_array = bit_array[(pos + 1) * 8:]
    ba = bitarray(arr)
    bit_list = ba.tolist()
    out_array = bitarray(bit_list).tobytes().decode('utf-8')

    dictionary = decompress_dict_modular(out_array)

    dictionary_keys = dictionary.keys()
    dictionary_vals = render_values(dictionary.values())

    dictionary = {key: bitarray(val) for key, val in zip(dictionary_keys, dictionary_vals)}

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
