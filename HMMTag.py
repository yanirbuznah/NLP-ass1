import sys
import time

import numpy as np
import utils

def vitterbiAlgorithm(lines, words_possible_tags):
    final_line_tags = []
    for line_number, line in enumerate(lines):
        v = [{(utils.START, utils.START): 1}]
        bp = []

        for i, word in enumerate(line):
            word = word.lower() if (word.lower() in words_possible_tags) else utils.word_sign(word)
            max_p = {}
            argmax_tag = {}
            for t_tag, t in v[i]:
                for r in words_possible_tags[word]:
                    e = utils.getE(word, r)
                    q = utils.interpulation(t_tag, t, r)
                    temp = v[i][(t_tag, t)] + np.log2(q) + np.log2(e)
                    if (t, r) not in max_p or temp > max_p[(t, r)]:
                        max_p[(t, r)] = temp
                        argmax_tag[(t, r)] = t_tag
            v.append(max_p)
            bp.append(argmax_tag)

        tags = get_line_tags(bp, v)
        final_line_tags.append(tags)

    return final_line_tags


def get_line_tags(bp, v):
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
    real_tags = utils.extract_tags_from_file('ass1-tagger-dev')
    best = 0
    for i in range(1000):
        x = np.random.random()
        y = np.random.random()
        z = np.random.random()
        s = x+y+z
        lambda1 = max(x/s,y/s)
        lambda2 = min(x/s,y/s)
        predicted_tags = vitterbiAlgorithm(lines, utils.get_dict(utils.emissions))

        accuracy = utils.calc_accuracy(predicted_tags, real_tags)
        if accuracy > best:
            best = accuracy
            print(f'lambda1: {lambda1},lambda2: {lambda2},lambda3: {1.0-lambda1-lambda2}')
            print(f"accuracy:  {str(accuracy)}")
    # input_tags = vitterbiAlgorithm(words, emissions, transitions, gt.get_dict(emissions),num_of_words)
    # # real_tags = gt.extract_tags_from_file('ass1-tagger-train')
    # accuracy = gt.accuracy(input_tags, real_tags)
    # print ("result: " + str(accuracy))
    # print(time.time() - start)
    # open(output_file_name, 'w').write(gt.tagInputData(inputData, inputTags))