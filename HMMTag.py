import sys
# from MLETrain import wordSign
from collections import defaultdict

import numpy as np

import MLETrain

transitions = {}
emissions = {}
tags = {}
num_of_words = 0


def ViterbiAlgorithm(lines, words_possible_tags):
    """
    greedy algorithm O(words*tags)
    returns: tags for data
    """
    lines_tags = []
    for line in lines:
        tag_i, t_minus_1, t_minus_2 = "*START*", "*START*", "*START*"
        line_tags = []
        for i, word in enumerate(line):
            if word not in words_possible_tags:
                word = word.lower() if (word.lower() in words_possible_tags) else word_sign(word)
            p_ti_wi = float('-inf')
            for t in words_possible_tags[word]:
                q = interpulation(t, t_minus_1, t_minus_2)
                e = getE(word, t)
                prob = np.log2(q) + np.log2(e)
                if prob > p_ti_wi:
                    p_ti_wi = prob
                    tag_i = t
            t_minus_2 = t_minus_1
            t_minus_1 = tag_i
            line_tags.append(tag_i)
        lines_tags.append(line_tags)
    return lines_tags


# e(w|t)
def getE(w, t):
    if (w, t) in emissions:
        # P(w|t) = Count(w,t) / Count(t)
        return emissions[(w, t)] / tags[t]
    else:
        return emissions[(MLETrain.UNK, t)] if (MLETrain.UNK, t) in emissions else 0


def interpulation(t1, t2, t3):
    """
    returns: p(c|a,b)
    """
    # lambda1 = 0.5
    # lambda2 = 0.3

    P_c_if_ab = transitions[(t1, t2, t3)] if (t1, t2, t3) in transitions else 0
    P_b_if_a = transitions[(t1, t2)] if (t1, t2) in transitions else 1
    P_c_if_b = transitions[(t2, t3)] if (t2, t3) in transitions else 0
    P_b = tags[t2] if t2 in tags else 1
    P_c = tags[t3] if t3 in tags else 0

    return lambda1 * float(P_c_if_ab) / float(P_b_if_a) \
           + lambda2 * float(P_c_if_b) / float(P_b) \
           + (1.0 - lambda2 - lambda1) * float(P_c) / num_of_words


def smooth(param):
    if param not in emissions:
        return 1 / sum(emissions.values())
    else:
        return float(emissions[param]) / float(tags[(param[1])])


def get_dict(e_mle):
    """
    makes a dictionary for each word the tags it can have
    q_mle_lines : q_mle
    returns: dictionary
    """

    d = defaultdict(set)
    for word, tag in e_mle:
        d[word].add(tag)
    return d


def parse_mle_file(file):
    mle = {}
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        key, val = line.rsplit("\t", 1)
        tags = tuple(key.split())
        mle[tags] = int(val)
    return mle


def lines_from_file(filePath):
    with open(filePath, 'r') as f:
        return f.readlines()


def words_from_file(filePath):
    return [line[:-1].split() for line in lines_from_file(filePath)]


def accuarcy(predcited_tags, real_tags):
    total = good = 0
    for i, line in enumerate(predcited_tags):
        for j, tag in enumerate(line):
            total += 1
            if tag == real_tags[i][j]:
                good += 1
    return float(good) / total


def extract_tags_from_file(test_file):
    def extract_tags(line):
        return [word_tag.rsplit('/', 1)[-1] for word_tag in line]

    seperated_lines = words_from_file(test_file)
    return [extract_tags(line) for line in seperated_lines]


def word_sign(word):
    # TODO: change to words signs like "UNK_ing" for example

    return word


def get_tags(emissions):
    tags = {}
    for e in emissions:
        tags[e[1]] = emissions[e] + tags[e[1]] if e[1] in tags else emissions[e]
    return tags


lambda1 = 0.0
lambda2 = 0.0

if __name__ == '__main__':
    input_file_name, q_mle_filename, e_mle_filename, output_file_name, extra_file = sys.argv[1:]
    words = words_from_file(input_file_name)
    transitions = parse_mle_file(q_mle_filename)
    emissions = parse_mle_file(e_mle_filename)
    tags = get_tags(emissions)
    num_of_words = sum(emissions.values())
    real_tags = extract_tags_from_file('ass1-tagger-dev')
    best = 0
    for i in range(1000):
        x = np.random.random()
        y = np.random.random()
        z = np.random.random()
        s = x + y + z
        lambda1 = max(x / s, y / s)
        lambda2 = min(x / s, y / s)
        predicted_tags = greedyAlgorithm(words, words_possible_tags=get_dict(emissions))
        accuracy = accuarcy(predicted_tags, real_tags)
        if accuracy > best:
            best = accuracy
            print(f'lambda1: {lambda1},lambda2: {lambda2},lambda3: {1.0 - lambda1 - lambda2}')
            print(f"accuracy:  {str(accuracy)}")
