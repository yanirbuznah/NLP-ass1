import sys
from collections import Counter

import numpy as np

import utils
from utils import *

def calc_mle(input_file_name):
    file = open(input_file_name, 'r')
    lines = file.readlines()
    file.close()
    words_tags = []
    for line in lines:
        # remove trailing '\n' and split by ' '
        tuples = [tuple(pair.rsplit('/', 1)) for pair in line.strip().split(' ')]
        words_tags += tuples
        split_line = line.strip().split(' ')
        calc_emle(split_line)
        calc_qmle(split_line)
    # rare_emissions = count_patterns(words_tags)
    # x = 43
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

def count_patterns(words_tags):
        unknown_token = utils.UNK
        num_occurrences = utils.THRESHOLD
        words_tags_counter = emissions
        # Count the number of occurrences of each word in the training set.
        counter = Counter([pair[0] for pair in words_tags])

        rare = set()

        # Collect the words in the training set that appear only once and consider them as rare wards.
        for word, amount in counter.items():
            if amount <= num_occurrences:
                rare.add(word)

        pattern_e_counts = Counter()

        # Go over each word and its associated tag that were found in the training set.
        for word, tag in set(words_tags):

            if word in rare:  # If the word is rare.

                # Find its fit word-signature pattern and update the word-signature count for its associated tag.
                signature = utils.word_sign(word) if utils.word_sign(word) is not None else unknown_token
                pattern_e_counts[(signature ,tag)] += words_tags_counter[(word,tag)]

            else:  # Otherwise

                # Find the fit word-signature pattern, if exists.
                signature = utils.word_sign(word)

                # If there is a word-signature pattern that fits.
                if signature is not None:
                    # Then update the word-signature count for the word's associated tag.
                    pattern_e_counts[(signature, tag)] += words_tags_counter[(word, tag)]

        return pattern_e_counts


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


# P(t3|t1, t2) = LMBDA1*P(t3|t1, t2) + LMBDA2*P(t3|t2) +  (1-LMBDA1-LMBDA2)*P(t3)
def getQ(t1, t2, t3):
    P_c_if_ab = transitions[(t1, t2, t3)] if (t1, t2, t3) in transitions else 1
    P_c_if_b = transitions[(t2, t3)] if (t2, t3) in transitions else 1
    P_c = transitions[(t3)] if t3 in transitions else 1

    interp = [P_c_if_ab, P_c_if_b, P_c]
    lambdas = [lambda1,lambda2,1-lambda1-lambda2]
    P = sum(LMBDA * p for LMBDA, p in zip(lambdas, interp))
    return np.log2(P)


# e(w|t)
def getE(w, t):
    if (w, t) in emissions:
        # P(w|t) = Count(w,t) / Count(t)
        return emissions[(w, t)] / tags[t]
    else:
        return emissions[(UNK, t)] if (UNK, t) in emissions else 0


def write_emle(emle):
    file = open(emle, 'w')
    for (w, t), count in emissions.items():
        file.write(f"{w} {t}\t{count}\n")
    file.close()


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
