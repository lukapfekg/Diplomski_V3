from collections import Counter


def str_to_array(string):
    out = []
    delimiters = "(), E"
    temp = str()
    for c in string:
        if c in delimiters:
            if temp != "":
                out.append(temp)
            out.append(c)
            temp = ""
        else:
            temp += c

    return out


def get_freq_dict(array: list) -> dict:
    data = Counter(array)
    # print(data.items())
    # output = {k: d / len(array) for k, d in data.items()}
    output = {k: d for k, d in data.items()}
    return output


def lowest_prob_pair(p):
    # Return pair of symbols from distribution p with lowest probabilities
    sorted_p = sorted(p.items(), key=lambda x: x[1])
    return sorted_p[0][0], sorted_p[1][0]


def find_huffman(p: dict) -> dict:
    """
    returns a Huffman code for an ensemble with distribution p
    :param dict p: frequency table
    :returns: huffman code for each symbol
    """
    # Base case of only two symbols, assign 0 or 1 arbitrarily; frequency does not matter
    if len(p) == 2:
        return dict(zip(p.keys(), ['0', '1']))

    # Create a new distribution by merging lowest probable pair
    p_prime = p.copy()
    a1, a2 = lowest_prob_pair(p)
    p1, p2 = p_prime.pop(a1), p_prime.pop(a2)
    p_prime[a1 + a2] = p1 + p2

    # Recurse and construct code on new distribution
    c = find_huffman(p_prime)
    ca1a2 = c.pop(a1 + a2)
    c[a1], c[a2] = ca1a2 + '0', ca1a2 + '1'

    return c


def huffman_decoding(input_string, dictionary):
    decoded = []
    codes = list(dictionary.values())
    temp = ''

    for c in input_string:
        temp += c

        if temp in codes:
            decoded.append(list(dictionary.keys())[codes.index(temp)])
            temp = ''

    return decoded


# s = "65 E 65 E (0,1)"
#
# freq = {'E': 22500, '(0,1)': 13835, '(0,-1)': 13776, '(0,2)': 7654, '(0,-2)': 7491, '(1,1)': 4928, '(1,-1)': 4832,
#         '(0,3)': 4778, '(0,-3)': 4771, '(0,-4)': 3566, '(0,4)': 3462, '(0,-5)': 2550, '(0,5)': 2540, '64': 2476,
#         '(2,-1)': 2286, '(2,1)': 2281, '(1,2)': 1896, '(1,-2)': 1829, '(0,6)': 1780, '(0,-6)': 1740, '(3,-1)': 1549,
#         '(3,1)': 1527, '(0,7)': 1495, '(0,-7)': 1439, '65': 1282, '0': 1251, '(0,-8)': 1248, '(0,8)': 1159,
#         '(4,1)': 999,
#         '(4,-1)': 967, '(0,9)': 952, '(0,-9)': 940, '(1,-3)': 878, '(0,10)': 867, '(1,3)': 863, '(0,-10)': 824,
#         '127': 770,
#         '(5,1)': 675, '(0,-11)': 674, '(0,-12)': 666, '(5,-1)': 649, '(0,11)': 623, '(0,18)': 251, '1': 248, '3': 247,
#         '(0,-18)': 241, '83': 240, '4': 237, '82': 235, '5': 235, '(1,-6)': 227, '(2,2)': 603, '(2,-2)': 595,
#         '(0,12)': 581, '(1,-4)': 512, '(0,13)': 507, '(6,-1)': 491, '(6,1)': 489, '(0,-13)': 486, '(1,4)': 471,
#         '126': 471,
#         '(0,14)': 449, '(0,-14)': 423, '79': 406, '(0,15)': 375, '125': 375, '(0,-15)': 369, '66': 351, '67': 348,
#         '(7,-1)': 346, '78': 344, '(0,-16)': 341, '80': 333, '(0,16)': 331, '77': 329, '124': 328, '(1,5)': 324,
#         '(7,1)': 322, '69': 318, '2': 318, '(0,-17)': 312, '(3,2)': 311, '76': 311, '81': 309, '(1,-5)': 305, '68': 295,
#         '75': 294, '74': 293, '72': 290, '(0,17)': 288, '73': 287, '70': 280, '123': 280, '(9,1)': 278, '(3,-2)': 273,
#         '(8,-1)': 271, '71': 267, '(8,1)': 262, '(9,-1)': 261, '(0,-19)': 256}
#
# f = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
# print(f)
