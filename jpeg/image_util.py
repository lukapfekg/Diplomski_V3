from pylab import *


def add_padding(img):
    h, w = img.shape

    if h % 8 == 0 and w % 8 == 0:
        return img

    else:
        pad_h = h % 8
        pad_w = w % 8

        img_out = np.zeros((h + pad_h, w + pad_w))

        img_out[:h, :w] = img

        if pad_h != 0:
            img_out[-pad_h:, :] = img_out[h - 1:h - pad_h - 1:-1, :]

        if pad_w != 0:
            img_out[:, -pad_w:] = img_out[:, w - 1:w - pad_w - 1:-1]

        return img_out


def resize_image(image):
    if len(shape(image)) == 2:
        h, w = image.shape
        if h % 8 == 0 and w % 8 == 0:
            return np.array(image)

        return add_padding(image)
    else:
        h, w, p = image.shape

        if h % 8 == 0 and w % 8 == 0:
            return image

        out_image = np.zeros((h + h % 8, w + w % 8, p))

        for i in range(p):
            out_image[:, :, i] = add_padding(image[:, :, i])

        return out_image
