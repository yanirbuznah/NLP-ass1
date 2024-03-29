import sys
from collections import Counter

import numpy as np

from utils import *

def calc_mle(input_file_name):
    file = open(input_file_name, 'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        split_line = line.strip().split(' ')
        calc_emle(split_line)
        calc_qmle(split_line)

    rare_emissions = {}
    for_remove = []
    for (w, t), value in emissions.items():
        if value <= THRESHOLD:
            new_key = word_sign(w)
            rare_emissions[(new_key, t)] = rare_emissions[(new_key, t)] + 1 if (new_key, t) in rare_emissions else 1
            for_remove.append((w, t))
    emissions.update(rare_emissions)
    for key in for_remove:
        emissions.pop(key)



def calc_qmle(split_line):
    # IN DT NNP -> [START,START,IN,DT,NNP,END]
    split_line.insert(0, f"{START}/{START}")
    split_line.insert(0, f"{START}/{START}")
    split_line.append(f"{END}/{END}")

    for i in range(len(split_line) - 2):
        # In/IN an/DT Oct./NNP -> [IN, DT, NNP]
        tagged_words = [split_line[j].rsplit('/', 1)[1] for j in range(i, i + 3)]
        bigram = (tagged_words[0], tagged_words[1])
        trigram = (tagged_words[0], tagged_words[1], tagged_words[2])
        # Count(t1, t2)
        transitions[bigram] = transitions[bigram] + 1 if bigram in transitions else 1
        # Count(t1, t2, t3)
        transitions[trigram] = transitions[trigram] + 1 if trigram in transitions else 1


def calc_emle(split_line):
    for tagged_word in split_line:
        tagged_word = tagged_word.rsplit('/', 1)
        word = tagged_word[0]
        tag = tagged_word[1]
        # count t
        tags[tag] = tags[tag] + 1 if tag in tags else 0
        # count w,t
        emissions[(word, tag)] =  emissions[(word, tag)] + 1 if (word, tag) in emissions else 1

def write_emle(emle):
    with open(emle, 'w') as file:
        for (w, t), count in emissions.items():
            file.write(f"{w} {t}\t{count}\n")


def write_qmle(qmle):
    file = open(qmle, 'w')
    for key, count in transitions.items():
        # bigram
        if len(key) == 2:
            file.write(f"{key[0]} {key[1]}\t{count}\n")
        # trigram
        elif len(key) == 3:
            file.write(f"{key[0]} {key[1]} {key[2]}\t{count}\n")
    for tag, count in tags.items():
        # unigram
        file.write(f"{tag}\t{count}\n")
    file.close()


def main():
    input_file_name = sys.argv[1]
    qmle = sys.argv[2]
    emle = sys.argv[3]
    calc_mle(input_file_name)
    write_emle(emle)
    write_qmle(qmle)


if __name__ == "__main__":
    main()