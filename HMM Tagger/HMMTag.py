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
    for i, word in enumerate(line):
        if word not in words_possible_tags:
            word = word.lower() if (word.lower() in words_possible_tags) else utils.word_sign(word)
        max_p = {}
        argmax_tag = {}
        for t2, t1 in v[i]:
            for t in sorted(words_possible_tags[word]):
                e = utils.smooth((word, t))
                q = utils.interpulation(t, t1, t2)

                temp = v[i][(t2, t1)] + np.log2(q) + np.log2(e)
                if (t1, t) not in max_p or temp > max_p[(t1, t)]:
                    max_p[(t1, t)] = temp
                    argmax_tag[(t1, t)] = t2
        v.append(max_p)
        bp.append(argmax_tag)


def get_best_tags_path(bp, v):
    # get the best tags
    before_last_tag, last_tag = max(v[-1], key=lambda tuple: tuple[-1])
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
    real_tags = utils.extract_tags_from_file('./ass1data/data/ass1-tagger-dev')
    best = 0
    utils.lambda1 = 0.8
    utils.lambda2 = 0.1
    predicted_tags = vitterbiAlgorithm(lines, utils.get_dict(utils.emissions))

    accuracy = utils.calc_accuracy(predicted_tags, real_tags)
    if accuracy > best:
        best = accuracy
        print(f'lambda1: {utils.lambda1},lambda2: {utils.lambda2},lambda3: {1.0 - utils.lambda1 - utils.lambda2}')
        print(f"accuracy:  {str(accuracy)}")
