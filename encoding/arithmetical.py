import decimal
from collections import Counter
from decimal import *
import time

import numpy as np

f = open("C:\\Users\\ll160389d\\PycharmProjects\\Diplomski_V3\\test\\eob_array.txt", 'r')

arr = f.readline()
arr = arr.split(' ')
f.close()

arr_len = len(arr)
print(arr_len)

decimal.getcontext().prec = decimal.MAX_PREC

data = Counter(arr)
dictionary = {k: Decimal(d / len(arr)) for k, d in data.items()}
print(dictionary)


# print('dict len -', len(dictionary))
#
#
# def compress_dict(dictionary):
#     out = dictionary.replace("'", "")
#     out = out.replace(" ", "")
#     return out
#
#
# d = compress_dict(str(dictionary))
# print('str len -', len(d))
# print('str len in bytes -', len(d) * 8)


def process_stage(probability_table, stage_min, stage_max):
    """
    Processing a stage in the encoding/decoding process.
    """
    stage_probs = {}
    stage_domain = stage_max - stage_min
    for term_idx in range(len(probability_table.items())):
        term = list(probability_table.keys())[term_idx]
        term_prob = probability_table[term]
        cum_prob = Decimal(term_prob * stage_domain + stage_min)
        stage_probs[term] = [stage_min, cum_prob]
        stage_min = cum_prob
    return stage_probs


def get_encoded_value(encoder):
    """
    After encoding the entire message, this method returns the single value that represents the entire message.
    """
    last_stage = list(encoder[-1].values())
    last_stage_values = []
    for sublist in last_stage:
        for element in sublist:
            last_stage_values.append(element)

    last_stage_min = min(last_stage_values)
    last_stage_max = max(last_stage_values)

    return (last_stage_min + last_stage_max) / 2


def encode(msg, probability_table):
    """
    Encodes a message.
    """

    encoder = []

    stage_min = Decimal(0.0)
    stage_max = Decimal(1.0)

    for elem in msg:
        stage_probs = process_stage(probability_table, stage_min, stage_max)

        stage_min = stage_probs[elem][0]
        stage_max = stage_probs[elem][1]

        encoder.append(stage_probs)

    stage_probs = process_stage(probability_table, stage_min, stage_max)
    encoder.append(stage_probs)

    encoded_msg = get_encoded_value(encoder)

    return encoder, encoded_msg


def decode(encoded_msg, msg_length, probability_table):
    """
    Decodes a message.
    """

    decoder = []
    decoded_msg = ""

    stage_min = Decimal(0.0)
    stage_max = Decimal(1.0)

    for idx in range(msg_length):
        stage_probs = process_stage(probability_table, stage_min, stage_max)

        for msg_term, value in stage_probs.items():
            if value[0] <= encoded_msg <= value[1]:
                break

        decoded_msg = decoded_msg + msg_term
        stage_min = stage_probs[msg_term][0]
        stage_max = stage_probs[msg_term][1]

        decoder.append(stage_probs)

    stage_probs = process_stage(probability_table, stage_min, stage_max)
    decoder.append(stage_probs)

    return decoder, decoded_msg


start = time.time()
encoder, encoded_msg = encode(arr, dictionary)

decoder, decoded_msg = decode(encoded_msg, len(arr), dictionary)
end = time.time()

print(decoded_msg)
print(end - start)
