import time

import numpy as np

zigzag_array_constant = np.array([[0, 1, 5, 6, 14, 15, 27, 28],
                                  [2, 4, 7, 13, 16, 26, 29, 42],
                                  [3, 8, 12, 17, 25, 30, 41, 43],
                                  [9, 11, 18, 24, 31, 40, 44, 53],
                                  [10, 19, 23, 32, 39, 45, 52, 54],
                                  [20, 22, 33, 38, 46, 51, 55, 60],
                                  [21, 34, 37, 47, 50, 56, 59, 61],
                                  [35, 36, 48, 49, 57, 58, 62, 63]])

zigzag_array_coordinates = [[0, 0], [0, 1], [1, 0], [2, 0], [1, 1], [0, 2], [0, 3], [1, 2], [2, 1], [3, 0], [4, 0],
                            [3, 1], [2, 2], [1, 3], [0, 4], [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0], [6, 0],
                            [5, 1], [4, 2], [3, 3], [2, 4], [1, 5], [0, 6], [0, 7], [1, 6], [2, 5], [3, 4], [4, 3],
                            [5, 2], [6, 1], [7, 0], [7, 1], [6, 2], [5, 3], [4, 4], [3, 5], [2, 6], [1, 7], [2, 7],
                            [3, 6], [4, 5], [5, 4], [6, 3], [7, 2], [7, 3], [6, 4], [5, 5], [4, 6], [3, 7], [4, 7],
                            [5, 6], [6, 5], [7, 4], [7, 5], [6, 6], [5, 7], [6, 7], [7, 6], [7, 7]]


def zigzag(arr, max_len=8):
    right = up_d = down = down_d = False
    start = True

    matrix = []

    i = j = 0

    while i < max_len or j < max_len:
        if start:
            start = False
            matrix.append(arr[i][j])
            right = True
            continue

        elif right:
            right = False
            if j == max_len - 1:
                down = True
            else:
                j += 1
                matrix.append(arr[i][j])
                down_d = True if i != max_len - 1 else False
                up_d = False if i != max_len - 1 else True

                if j == max_len - 1 and i == max_len - 1:
                    break

            continue

        elif down:
            down = False
            if i == max_len - 1:
                right = True
            else:
                i += 1
                matrix.append(arr[i][j])
                up_d = True if j != max_len - 1 else False
                down_d = False if j != max_len - 1 else True
            continue

        elif down_d:
            # TODO: rewrite after all works
            down_d = False
            if i == max_len - 1 or j == 0:
                down = True

            else:
                i += 1
                j -= 1
                matrix.append(arr[i][j])
                down_d = True
            continue

        elif up_d:
            up_d = False

            if i == 0 or j == max_len - 1:
                right = True

            else:
                i -= 1
                j += 1
                matrix.append(arr[i][j])
                up_d = True
            continue

    return matrix


def inverse_zigzag(arr, max_len=8):
    right = up_d = down = down_d = False
    start = True

    out_matrix = np.zeros((8, 8))

    i = j = 0
    arr_index = 0

    while i < max_len or j < max_len:
        if start:
            start = False
            out_matrix[i, j] = arr[arr_index]
            arr_index += 1
            right = True
            continue

        elif right:
            right = False
            if j == max_len - 1:
                down = True
            else:
                j += 1
                out_matrix[i, j] = arr[arr_index]
                arr_index += 1
                down_d = True if i != max_len - 1 else False
                up_d = False if i != max_len - 1 else True

                if j == max_len - 1 and i == max_len - 1:
                    break

            continue

        elif down:
            down = False
            if i == max_len - 1:
                right = True
            else:
                i += 1
                out_matrix[i, j] = arr[arr_index]
                arr_index += 1
                up_d = True if j != max_len - 1 else False
                down_d = False if j != max_len - 1 else True
            continue

        elif down_d:
            # TODO: rewrite after all works
            down_d = False
            if i == max_len - 1 or j == 0:
                down = True

            else:
                i += 1
                j -= 1
                out_matrix[i, j] = arr[arr_index]
                arr_index += 1
                down_d = True
            continue

        elif up_d:
            up_d = False

            if i == 0 or j == max_len - 1:
                right = True

            else:
                i -= 1
                j += 1
                out_matrix[i, j] = arr[arr_index]
                arr_index += 1
                up_d = True
            continue

    return out_matrix


def get_zigzag_array(dct_image):
    zigzag_arr = []
    for elem in dct_image:
        zigzag_arr.append(zigzag(elem))

    return zigzag_arr


def zigzag_optimized(array):
    out = []

    for i, j in zigzag_array_coordinates:
        out.append(array[i, j])

    return out


def get_zigzag_optimized(dct_image, tred=False):
    zigzag_arr = []
    for elem in dct_image:
        zigzag_arr.append(zigzag_optimized(elem))

    if tred:
        print('yee')

    return zigzag_arr

#
# start = time.time()
# print(zigzag_optimized(zigzag_array_constant))
# end = time.time()
# print(end - start)
#
# start = time.time()
# print(zigzag(zigzag_array_constant))
# end = time.time()
# print(end - start)
