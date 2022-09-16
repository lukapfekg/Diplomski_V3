from pylab import *


def add_padding(img, block_size=8):
    h, w = img.shape

    if h % block_size == 0 and w % block_size == 0:
        return img

    else:
        pad_h = 0 if h % block_size == 0 else block_size - h % block_size
        pad_w = 0 if w % block_size == 0 else block_size - w % block_size

        img_out = np.zeros((h + pad_h, w + pad_w))

        img_out[:h, :w] = img

        if pad_h != 0:
            img_out[-pad_h:, :] = img_out[h - 1:h - pad_h - 1:-1, :]

        if pad_w != 0:
            img_out[:, -pad_w:] = img_out[:, w - 1:w - pad_w - 1:-1]

        return img_out


def resize_image(image, block_size=8):
    if len(shape(image)) == 2:
        h, w = image.shape
        if h % block_size == 0 and w % block_size == 0:
            return np.array(image)

        return add_padding(image)

    else:
        h, w, p = image.shape

        if h % block_size == 0 and w % block_size == 0:
            return image

        pad_h = 0 if h % block_size == 0 else block_size - h % block_size
        pad_w = 0 if w % block_size == 0 else block_size - w % block_size

        out_image = np.zeros((h + pad_h, w + pad_w, p))

        for i in range(p):
            out_image[:, :, i] = add_padding(image[:, :, i])

        return out_image

#
# image = imread("../Examples/miner.jpg")
# print(image.shape)
# img = resize_image(image, block_size=4)
# print(img.shape)
