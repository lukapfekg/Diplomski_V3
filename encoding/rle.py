from itertools import groupby
import numpy as np
import re

mes = [1, 2, 3, 4, 0, 0, 0, 5, 5, 6, -1, 2, 6, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]


def find_eob(array):
    for i in range(len(array) - 1, 0, -1):
        if array[i] == 0:
            array = array[:-1]
        else:
            break

    return np.append(array, 'E')


def run_length_encoder(array):
    out = []
    cnt = 0
    last = '.'
    for i in range(len(array)):
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
    # TODO: Add last rle if no EOL
    # out = "".join(out)
    return out


def run_length_encoder_2(array):
    out_list = []
    num_cnt = 0
    zero_cnt = 0
    last = '.'

    for elem in array:
        if len(out_list) == 0:
            out_list.append(elem)

        elif elem == 'E':
            if last != '.':
                out_list.append('(' + str(zero_cnt) + ',' + str(num_cnt) + ',' + last + ')')

            out_list.append(elem)
            return out_list

        elif elem == '0':
            if last == '0' or last == '.':
                zero_cnt += 1
                last = '0'
            else:
                out_list.append('(' + str(zero_cnt) + ',' + str(num_cnt) + ',' + last + ')')
                zero_cnt = 1
                last = '0'

        else:
            if last == elem:
                num_cnt += 1
            else:
                if last != '.' and last != '0':
                    out_list.append('(' + str(zero_cnt) + ',' + str(num_cnt) + ',' + last + ')')
                    zero_cnt = 0
                num_cnt = 0
                last = str(elem)

    # out = "".join(out)
    return out_list


def run_length_decoder(string: str):
    rle = re.split(r'\(|\)', string)
    print(rle)
    rle = [e for e in rle if e != '']
    print(rle)
    out = []

    for elem in rle:

        if ',' not in elem:
            if elem == 'E':
                l = len(out)
                for i in range(64 - l):
                    out.append('0')
            else:
                out.append(elem)
        else:
            temp = elem.split(',')
            mul = int(temp[0])
            num = temp[1]
            out.append(num)
            for i in range(mul):
                out.append(num)

    return out


def find_rle(arr, rle_type=1):
    rle_array = []
    for elem in arr:
        eob = find_eob(elem)
        if rle_type == 1:
            eob = run_length_encoder(eob)
        elif rle_type == 2:
            eob = run_length_encoder_2(eob)

        rle_array += eob

    return rle_array


# eob = find_eob(mes)
# print(eob)
#
# rle = run_length_encoder(eob)
# print(rle)
# rle = "".join(rle)
# print(rle)
#
# decoded = run_length_decoder(rle)
# decoded = [int(i) for i in decoded]
# print(decoded)
# print(len(decoded))


a = ['a', 'b', 'c']
b = ['d', 'e']

print(a)
a += b
print(a)
