from numpy import *


def lzw_coding(array):
    arr = np.array(array)
    arr = arr.flatten()

    dict_size = 256

    dictionary = [[i] for i in range(256)]

    seq = []
    new_seq = []
    out = []

    for num in arr:
        new_seq = seq.copy()
        new_seq.append(num)

        if new_seq in dictionary:
            seq = new_seq.copy()
        else:
            out.append(dictionary.index(seq))
            dictionary.append(new_seq)
            seq.clear()
            seq.append(num)

    if seq:
        out.append(dictionary.index(seq))

    return out, dictionary


def lzw_decoding(arr, dictionary):
    out = []

    for num in arr:
        elem = dictionary[num]
        out.append(elem)

    out = [element for sublist in out for element in sublist]

    return out
