import time

from pylab import *

import skimage
from skimage import color
from skimage import exposure
from skimage import filters
from skimage import io
from skimage import util
from skimage import morphology

from scipy import ndimage
from skimage import restoration

import numpy as np


# add_padding je funkcija koja prosiruje sliku mirror-ovanjem redova i kolona

# img - input, 2d array, ulazna slika
# pad - input, integer, sirina prosirenja po jednoj osi

# img_out - output, 2d array, prosirena slika
def add_padding(img, pad):
    # izlazna slika se prosiri sa 2*pad
    img_out = np.zeros((img.shape[0] + 2 * pad, img.shape[1] + 2 * pad))
    # zatim se u sredinu slike postavi ulazna slika
    img_out[pad:-pad, pad:-pad] = img

    # po x osi se mirror-uju odredjeni redovi ulazne slike
    img_out[0:pad, pad:-pad] = img[pad - 1::-1, :]
    img_out[-pad:, pad:-pad] = img[:-pad - 1:-1, :]

    # po y osi se miror-uju odredjene kolone izlazne slike
    img_out[:, :pad] = img_out[:, 2 * pad:pad:-1]
    img_out[:, :-pad - 1:-1] = img_out[:, -2 * pad:-pad]

    return img_out


# get_median_pixel

# img - input, 2d array, ulazna slika
# x, y - input, integer, koordinate datog piksela
# s_max - input, integer, maksimalna velicina prozora

# median - output, median prozora, nova vrednost datog piksela
def get_median_pixel(img, x, y, s_max):
    # odrede se velicine prozora sa leve i desne strane datog piksela
    mask_left = math.floor(s_max / 2)
    # kod mask_right se broj zaokruzuje na visu cifru
    # zbog prirode indeksiranja matrice, ako stavimo arr[:5] gledace se vrednosti do indeksa 5, a ne i indeks 5
    mask_right = math.ceil(s_max / 2)

    # odrede se koordinate krajnjih piksela prozora
    upper_left_x = x - mask_left
    upper_left_y = y - mask_left

    down_right_x = x + mask_right
    down_right_y = y + mask_right

    # uzme se prozor slike
    window = img[upper_left_x:down_right_x, upper_left_y:down_right_y]

    # izracuna se medijan
    median = np.median(window)

    return median


# get_median_pixel_adaptive je funkcija za izracunavanje vrednosti trenutnog piksela

# img - input, 2d array, ulazna slika
# x, y - input, integer, koordinate datog piksela
# s - input, integer, trenutna velicina prozora
# s_max - input, integer, maksimalna velicina prozora

# out_pix - output, nova vrednost datog piksela

def get_median_pixel_adaptive(img, x, y, s, s_max):
    # odrede se velicine prozora sa leve i desne strane datog piksela
    mask_left = math.floor(s / 2)
    # kod mask_right se broj zaokruzuje na visu cifru
    # zbog prirode indeksiranja matrice, ako stavimo arr[:5] gledace se vrednosti do indeksa 5, a ne i indeks 5
    mask_right = math.ceil(s / 2)

    # odrede se koordinate krajnjih piksela prozora
    upper_left_x = x - mask_left
    upper_left_y = y - mask_left

    down_right_x = x + mask_right
    down_right_y = y + mask_right

    # uzme se prozor slike
    mask = img[upper_left_x:down_right_x, upper_left_y:down_right_y]

    # odrede se medijan, minimum i maksimum prozora
    median = np.median(mask)
    min_ = np.min(mask)
    max_ = np.max(mask)

    # out_pix predstavlja trenutnu vrednost piksela
    out_pix = img[x, y]

    # prvi uslov adaptivnog medijan filtra
    # ako je medijan prozora jednak minimumu ili maksimumu
    # prozor se prosiruje i funkcija se ponovo poziva
    if median == min_ or median == max_:
        if s < s_max:
            out_pix = get_median_pixel_adaptive(img, x, y, s + 2, s_max)

    # ako trenutni piksel minimum ili maksimum prozora vrednost mu se menja medijanom
    elif out_pix == min_ or out_pix == max_ or s == s_max:
        out_pix = median

    return out_pix


def dos_median(img_in, s_max, adaptive=False):
    # proverava se da li je slika 2d ili 3d niz
    i = len(img_in.shape)

    if i == 2:
        img_float = skimage.img_as_float(img_in)

        # padding je polovina maksimalne sirine prozora
        padding = s_max // 2
        # slika se prosiri
        padded_image = add_padding(img_float, padding)

        height, width = img_in.shape

        img_out = np.zeros(img_in.shape)

        # prolazi se kroz svaki piksel ponaosob
        # u zavisnosti da li je adaptiv True ili False
        # poziva se odgovarajuca funkcija
        for x in np.arange(height):
            for y in np.arange(width):
                # za koordinate piksela se prosledjuju koordinate sa '+ padding'
                # jer je padded image prosirena slika, a mi zelimo da usrednjimo
                # samo ulaznu sliku, ne i prosirenu
                img_out[x, y] = get_median_pixel(padded_image, x + padding, y + padding,
                                                 s_max) if adaptive == False else get_median_pixel_adaptive(
                    padded_image, x + padding, y + padding, 3, s_max)

        return img_out

    if i == 3:
        # slika je 3d niz, za svaku ravan se poziva pnovo dos_median

        # ako se prosledi 3d slika, pretpostavka je da je u RGB formatu
        img_in_gray = color.rgb2gray(img_in)

        img_out = np.zeros(img_in_gray.shape)

        img_out = dos_median(img_in_gray, s_max, adaptive)

        return img_out


image = imread("../test/Y_after_compression.jpg")
image = color.rgb2gray(image).astype(np.uint8)

start = time.time()
filtered_image = dos_median(image, 5, True)
end = time.time()
print(end - start)

filtered_image = color.gray2rgb(filtered_image)


imsave("filtered.jpg", filtered_image)