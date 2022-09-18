import numpy as np
from numpy import shape, meshgrid

from jpeg.dct import QUANTIZATION_MATRIX


def bilinear_interpolation(img_in, scale):
    [height_in, width_in] = shape(img_in)

    height_out = round(scale * height_in)
    width_out = round(scale * width_in)

    x_out = range(0, width_out)
    y_out = range(0, height_out)

    x_in = np.asarray([(x / scale) for x in x_out])
    y_in = np.asarray([(y / scale) for y in y_out])

    x_in_0 = np.floor(x_in).astype(int);
    x_in_1 = x_in_0 + 1
    x_in_0 = np.clip(x_in_0, 0, width_in - 1);
    x_in_1 = np.clip(x_in_1, 0, width_in - 1);

    y_in_0 = np.floor(y_in).astype(int);
    y_in_1 = y_in_0 + 1
    y_in_0 = np.clip(y_in_0, 0, height_in - 1);
    y_in_1 = np.clip(y_in_1, 0, height_in - 1);

    X0, Y0 = meshgrid(x_in_0, y_in_0)
    X1, Y1 = meshgrid(x_in_1, y_in_1)
    X, Y = meshgrid(x_in, y_in)

    img_in_A = img_in[Y0, X0]
    img_in_B = img_in[Y0, X1]
    img_in_C = img_in[Y1, X0]
    img_in_D = img_in[Y1, X1]

    w_x = X1 - X
    w_y = Y1 - Y

    img_out = w_y * (w_x * img_in_A + (1 - w_x) * img_in_B) + (1 - w_y) * (w_x * img_in_C + (1 - w_x) * img_in_D)

    return img_out.astype(np.uint8)

