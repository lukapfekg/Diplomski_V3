import time

import numpy as np

zigzag_array_constant_4 = np.array([[0, 1, 5, 6],
                                    [2, 4, 7, 12],
                                    [3, 8, 11, 13],
                                    [9, 10, 14, 15]])

zigzag_array_constant_8 = np.array([[0, 1, 5, 6, 14, 15, 27, 28],
                                    [2, 4, 7, 13, 16, 26, 29, 42],
                                    [3, 8, 12, 17, 25, 30, 41, 43],
                                    [9, 11, 18, 24, 31, 40, 44, 53],
                                    [10, 19, 23, 32, 39, 45, 52, 54],
                                    [20, 22, 33, 38, 46, 51, 55, 60],
                                    [21, 34, 37, 47, 50, 56, 59, 61],
                                    [35, 36, 48, 49, 57, 58, 62, 63]])

zigzag_array_constant_16 = np.array([[0, 1, 5, 6, 14, 15, 27, 28, 44, 45, 65, 66, 90, 91, 119, 120],
                                     [2, 4, 7, 13, 16, 26, 29, 43, 46, 64, 67, 89, 92, 118, 121, 150],
                                     [3, 8, 12, 17, 25, 30, 42, 47, 63, 68, 88, 93, 117, 122, 149, 151],
                                     [9, 11, 18, 24, 31, 41, 48, 62, 69, 87, 94, 116, 123, 148, 152, 177],
                                     [10, 19, 23, 32, 40, 49, 61, 70, 86, 95, 115, 124, 147, 153, 176, 178],
                                     [20, 22, 33, 39, 50, 60, 71, 85, 96, 114, 125, 146, 154, 175, 179, 200],
                                     [21, 34, 38, 51, 59, 72, 84, 97, 113, 126, 145, 155, 174, 180, 199, 201],
                                     [35, 37, 52, 58, 73, 83, 98, 112, 127, 144, 156, 173, 181, 198, 202, 219],
                                     [36, 53, 57, 74, 82, 99, 111, 128, 143, 157, 172, 182, 197, 203, 218, 220],
                                     [54, 56, 75, 81, 100, 110, 129, 142, 158, 171, 183, 196, 204, 217, 221, 234],
                                     [55, 76, 80, 101, 109, 130, 141, 159, 170, 184, 195, 205, 216, 222, 233, 235],
                                     [77, 79, 102, 108, 131, 140, 160, 169, 185, 194, 206, 215, 223, 232, 236, 245],
                                     [78, 103, 107, 132, 139, 161, 168, 186, 193, 207, 214, 224, 231, 237, 244, 246],
                                     [104, 106, 133, 138, 162, 167, 187, 192, 208, 213, 225, 230, 238, 243, 247, 252],
                                     [105, 134, 137, 163, 166, 188, 191, 209, 212, 226, 229, 239, 242, 248, 251, 253],
                                     [135, 136, 164, 165, 189, 190, 210, 211, 227, 228, 240, 241, 249, 250, 254, 255]])

zigzag_array_coordinates_4 = [[0, 0], [0, 1], [1, 0], [2, 0], [1, 1], [0, 2], [0, 3], [1, 2], [2, 1], [3, 0], [3, 1],
                              [2, 2], [1, 3], [2, 3], [3, 2], [3, 3]]

zigzag_array_coordinates_8 = [[0, 0], [0, 1], [1, 0], [2, 0], [1, 1], [0, 2], [0, 3], [1, 2], [2, 1], [3, 0], [4, 0],
                              [3, 1], [2, 2], [1, 3], [0, 4], [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0], [6, 0],
                              [5, 1], [4, 2], [3, 3], [2, 4], [1, 5], [0, 6], [0, 7], [1, 6], [2, 5], [3, 4], [4, 3],
                              [5, 2], [6, 1], [7, 0], [7, 1], [6, 2], [5, 3], [4, 4], [3, 5], [2, 6], [1, 7], [2, 7],
                              [3, 6], [4, 5], [5, 4], [6, 3], [7, 2], [7, 3], [6, 4], [5, 5], [4, 6], [3, 7], [4, 7],
                              [5, 6], [6, 5], [7, 4], [7, 5], [6, 6], [5, 7], [6, 7], [7, 6], [7, 7]]

zigzag_array_coordinates_16 = [[0, 0], [0, 1], [1, 0], [2, 0], [1, 1], [0, 2], [0, 3], [1, 2], [2, 1], [3, 0], [4, 0],
                               [3, 1], [2, 2], [1, 3], [0, 4],
                               [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0], [6, 0], [5, 1], [4, 2], [3, 3], [2, 4],
                               [1, 5], [0, 6], [0, 7], [1, 6],
                               [2, 5], [3, 4], [4, 3], [5, 2], [6, 1], [7, 0], [8, 0], [7, 1], [6, 2], [5, 3], [4, 4],
                               [3, 5], [2, 6], [1, 7], [0, 8],
                               [0, 9], [1, 8], [2, 7], [3, 6], [4, 5], [5, 4], [6, 3], [7, 2], [8, 1], [9, 0], [10, 0],
                               [9, 1], [8, 2], [7, 3],
                               [6, 4], [5, 5], [4, 6], [3, 7], [2, 8], [1, 9], [0, 10], [0, 11], [1, 10], [2, 9],
                               [3, 8], [4, 7], [5, 6], [6, 5],
                               [7, 4], [8, 3], [9, 2], [10, 1], [11, 0], [12, 0], [11, 1], [10, 2], [9, 3], [8, 4],
                               [7, 5], [6, 6], [5, 7], [4, 8],
                               [3, 9], [2, 10], [1, 11], [0, 12], [0, 13], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8],
                               [6, 7], [7, 6], [8, 5], [9, 4],
                               [10, 3], [11, 2], [12, 1], [13, 0], [14, 0], [13, 1], [12, 2], [11, 3], [10, 4], [9, 5],
                               [8, 6], [7, 7], [6, 8],
                               [5, 9], [4, 10], [3, 11], [2, 12], [1, 13], [0, 14], [0, 15], [1, 14], [2, 13], [3, 12],
                               [4, 11], [5, 10], [6, 9],
                               [7, 8], [8, 7], [9, 6], [10, 5], [11, 4], [12, 3], [13, 2], [14, 1], [15, 0], [15, 1],
                               [14, 2], [13, 3], [12, 4],
                               [11, 5], [10, 6], [9, 7], [8, 8], [7, 9], [6, 10], [5, 11], [4, 12], [3, 13], [2, 14],
                               [1, 15], [2, 15], [3, 14],
                               [4, 13], [5, 12], [6, 11], [7, 10], [8, 9], [9, 8], [10, 7], [11, 6], [12, 5], [13, 4],
                               [14, 3], [15, 2], [15, 3],
                               [14, 4], [13, 5], [12, 6], [11, 7], [10, 8], [9, 9], [8, 10], [7, 11], [6, 12], [5, 13],
                               [4, 14], [3, 15], [4, 15],
                               [5, 14], [6, 13], [7, 12], [8, 11], [9, 10], [10, 9], [11, 8], [12, 7], [13, 6], [14, 5],
                               [15, 4], [15, 5], [14, 6],
                               [13, 7], [12, 8], [11, 9], [10, 10], [9, 11], [8, 12], [7, 13], [6, 14], [5, 15],
                               [6, 15], [7, 14], [8, 13], [9, 12],
                               [10, 11], [11, 10], [12, 9], [13, 8], [14, 7], [15, 6], [15, 7], [14, 8], [13, 9],
                               [12, 10], [11, 11], [10, 12],
                               [9, 13], [8, 14], [7, 15], [8, 15], [9, 14], [10, 13], [11, 12], [12, 11], [13, 10],
                               [14, 9], [15, 8], [15, 9],
                               [14, 10], [13, 11], [12, 12], [11, 13], [10, 14], [9, 15], [10, 15], [11, 14], [12, 13],
                               [13, 12], [14, 11], [15, 10],
                               [15, 11], [14, 12], [13, 13], [12, 14], [11, 15], [12, 15], [13, 14], [14, 13], [15, 12],
                               [15, 13], [14, 14], [13, 15],
                               [14, 15], [15, 14], [15, 15]]


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

    out_matrix = np.zeros((max_len, max_len))

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


def zigzag_optimized(array, block_size = 8):
    out = []

    coord = zigzag_array_coordinates_8 if block_size == 8 else (
        zigzag_array_coordinates_4 if block_size == 4 else zigzag_array_coordinates_16)

    for i, j in coord:
        out.append(array[i, j])

    return out


# def inverse_zigzag_optimized(array, block_size):
#     out_array = np.zeros((block_size, block_size)).astype(int)
#
#     coord = zigzag_array_coordinates_8 if block_size == 8 else (
#         zigzag_array_coordinates_4 if block_size == 4 else zigzag_array_coordinates_16)
#
#     out = []
#     for elem in array:
#         for i, e in enumerate(elem):
#             x, y = coord[i]
#             out_array[x, y] = e
#
#         out.append(out_array)
#         out_array = np.zeros((block_size, block_size)).astype(int)
#     return out


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

# arr = [i for i in range(64)]
# a = []
# a.append(arr)
# a.append(arr)
# print(arr)
#
# inv = inverse_zigzag_optimized(a, 8)
#
# print(inv)

# f = open('rle.txt', 'w')
#
# f.write('[')
# for i in range(4):
#     f.write('[')
#     for j in range(4):
#         f.write(str(out[i, j]))
#         if j < 3:
#             f.write(', ')
#
#     if i < 3:
#         f.write('], \n')
#
# f.write(']')
# f.close()
