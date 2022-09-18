import numpy as np
import re


def find_eob(array):
    cnt = 0
    array = np.array(array).astype(str)
    for i in range(len(array) - 1, 0, -1):
        if array[i] == '0':
            cnt += 1
            array = array[:-1]
        else:
            break

    if cnt > 0:
        return np.append(array, 'E')
    else:
        return array


def rle_encoder_modular_z(array):
    out = []
    cnt = 0

    for i, elem in enumerate(array):
        if i == 0:
            out.append(elem)

        elif elem == 'E':
            out.append(elem)
            return out

        elif elem == '0':
            cnt += 1

        else:
            out.append('(' + str(cnt) + ',' + elem + ')')
            cnt = 0

    return out


def rle_encoder_modular_n(array):
    out = []
    cnt = 0
    last = '.'
    for i, elem in enumerate(array):
        if i == 0:
            out.append(array[i])

        elif array[i] == 'E':
            if last != '.':
                out.append('(' + str(cnt) + ',' + last + ')')

            out.append(array[i])
            return out

        else:
            if last == array[i]:
                cnt += 1

            else:
                if last != '.':
                    out.append('(' + str(cnt) + ',' + last + ')')
                cnt = 0
                last = str(array[i])

    out.append('(' + str(cnt) + ',' + last + ')')
    return out


def rle_encoder_modular(array):
    out = []
    cnt = 0
    last = array[0]
    for elem in array:
        if last == elem:
            cnt += 1
        else:
            out.append('(' + str(cnt) + ',' + last + ')')
            last = elem
            cnt = 1

    out.append('(' + str(cnt) + ',' + last + ')')

    return out


def rle_modular(array, dct=True):
    out = []
    if dct:
        for elem in array:
            eob = find_eob(elem)
            rle = rle_encoder_modular_z(eob)
            out += rle

    else:
        out = rle_encoder_modular(array)

    return out


# # mes = [1, 2, 3, 4, 0, 0, 0, 5, 5, 6, -1, 2, 6, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
# mes = [[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]
#
# arr = [str(i) for i in mes]
#
# rle_arr = rle_modular(mes)
#
# print(rle_arr)
