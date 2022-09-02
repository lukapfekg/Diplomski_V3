import json

from pylab import *


def parse_to_dict(dictionary):
    out = ''
    for c in dictionary:
        if c == '{':
            out += c + "\""
        elif c == '}':
            out += "\"" + c
        elif c == ':':
            out += "\"" + c + " \""
        elif c == ',':
            out += "\"" + c + " \""
        else:
            out += c

    lst = out.split("\"\"")
    out = lst[0] + "\" \"" + lst[1]

    return out


def parse_to_dict2(dictionary):
    out = ''
    inside = False
    for c in dictionary:
        if c == '(':
            inside = True
            out += c
        elif c == ')':
            inside = False
            out += c
        elif c == '{':
            out += c + "\""
        elif c == '}':
            out += "\"" + c
        elif c == ':':
            out += "\"" + c + " \""
        elif c == ',':
            out += "\"" + c + " \"" if inside is False else c
        else:
            out += c

    # lst = out.split("\"\"")
    # out = lst[0] + "\" \"" + lst[1]

    return out


def compress_dict(dictionary):
    out = dictionary.replace("'", "")
    out = out.replace(" ", "")
    return out


def string_to_ascii(dictionary):
    out_bin = str()
    for c in dictionary:
        temp = ord(c)
        temp = '{0:08b}'.format(ord(c))
        out_bin += temp

    return out_bin


def binary_to_dict(binary):
    inp = str()
    prev = ''
    i = 0
    while prev != '}':
        temp = str(binary[i * 8: i * 8 + 8])
        temp = int(temp, 2)
        temp = chr(temp)
        inp += temp
        prev = temp
        i += 1

    inp = parse_to_dict2(inp)
    inp = json.loads(inp)
    return inp, i * 8
