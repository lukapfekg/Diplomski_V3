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

# mes = '1(0,2)(0,3)(0,4)(2,0)(1,5)(0,6)(0,-1)(0,2)(0,6)(4,0)(0,1)E'
# arr_mes = ['1', '(0,2)', '(0,3)', '(0,4)', '(2,0)', '(1,5)', '(0,6)', '(0,-1)', '(0,2)', '(0,6)', '(4,0)', '(0,1)', 'E']
#
# print(len(mes) * 8)
#
# mes_arr = str_to_array(mes)
# print(mes_arr)
#
# print()
# print("freq")
# freq = get_freq_dict(mes_arr)
# freq2 = get_freq_dict(arr_mes)
# print(freq)
# print(len(freq))
# print(freq2)
# print(len(freq2))
#
# print()
# print("huff")
# huff = find_huffman(freq)
# huff2 = find_huffman(freq2)
# print(huff)
# print(len(huff))
# print(huff2)
# print(len(huff2))
#
# print()
# print("code")
# huff_code = ""
# huff_code2 = ""
# for i in mes_arr:
#     huff_code += huff[i]
#
# for i in arr_mes:
#     huff_code2 += huff2[i]
#
#
# print(huff_code)
# print(len(huff_code))
# print(huff_code2)
# print(len(huff_code2))
#
# decoded = huffman_decoding(huff_code, huff)
#
# print("".join(decoded))
