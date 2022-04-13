import sys
import time

import numpy as np

import utils


def vitterbiAlgorithm(lines, words_possible_tags):
    final_line_tags = []
    for line_number, line in enumerate(lines):
        v = [{(utils.START, utils.START): 1}]
        bp = []

        viterbi_on_single_line(bp, line, v, words_possible_tags)

        tags = get_best_tags_path(bp, v)
        final_line_tags.append(tags)

    return final_line_tags


def viterbi_on_single_line(bp, line, v, words_possible_tags):
    for i, word in enumerate(line):  # n
        if word not in words_possible_tags:
            word = word.lower() if (word.lower() in words_possible_tags) else utils.word_sign(word)
        max_p = {}
        argmax_tag = {}
        for t2, t1 in v[i]:  # O(|T|^2)
            for t in sorted(words_possible_tags[word]):  # O(|T|)
                e = utils.getE(word, t)
                q = utils.interpulation(t, t1, t2)
                temp = v[i][(t2, t1)] + np.log(q) + np.log(e)
                if (t1, t) not in max_p or temp > max_p[(t1, t)]:
                    max_p[(t1, t)] = temp
                    argmax_tag[(t1, t)] = t2

        v.append(max_p)
        bp.append(argmax_tag)


def get_best_tags_path(bp, v):
    before_last_tag, last_tag = max(v[-1])
    best = float('-inf')
    for t2, t1 in v[-1]:
        q = max(utils.interpulation(utils.END, t1, t2), 1e-6)  # ignore divide by zero

        temp = v[-1][(t2, t1)] + np.log(q)
        if best < temp:
            best = temp
            before_last_tag = t2
            last_tag = t1

    tags = [last_tag] + [before_last_tag] if before_last_tag != utils.START else [last_tag]

    for j in range(len(v) - 2, 1, -1):
        prev_t = bp[j][(before_last_tag, last_tag)]
        tags.append(prev_t)
        last_tag = before_last_tag
        before_last_tag = prev_t
    tags.reverse()
    return tags


if __name__ == '__main__':
    start = time.time()
    input_file_name, q_mle_filename, e_mle_filename, output_file_name, extra_file = sys.argv[1:]
    lines = utils.seperated_lines_from_file(input_file_name)
    utils.transitions = utils.parse_mle_file(q_mle_filename)
    utils.emissions = utils.parse_mle_file(e_mle_filename)
    utils.tags = utils.get_tags(utils.emissions)
    utils.num_of_words = sum(utils.emissions.values())
    best = 0

    if 'O' in utils.tags:  # ner task
        utils.lambda1 = 0.2
        utils.lambda2 = 0.18
    else:
        utils.lambda1 = 0.8
        utils.lambda2 = 0.1

    predicted_tags = vitterbiAlgorithm(lines, utils.get_dict(utils.emissions))
    utils.write_output_file(predicted_tags, lines, output_file_name)
