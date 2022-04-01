import sys
# from MLETrain import wordSign

import numpy as np
import utils



def greedyAlgorithm(lines, words_possible_tags):
    """
    greedy algorithm O(words*tags)
    returns: tags for data
    """
    """
    pseudo:
        check if word is name or just start of sentence by checking if the word exist in lower case
        if the word not in the dictionary, find the word sign (for example: *UNK*_ing)
        check the best prob by greedy search:
            use lidston smoothing and interpolation to find the probs and get the best if them
    
    """
    lines_tags = []
    for line in lines:
        tag_i, t_minus_1, t_minus_2 = "*START*", "*START*", "*START*"
        line_tags = []
        for i, word in enumerate(line):
            if word not in words_possible_tags:
                word = word.lower() if (word.lower() in words_possible_tags) else utils.word_sign(word)
            p_ti_wi = float('-inf')
            for t in words_possible_tags[word]:
                q = utils.interpulation(t, t_minus_1, t_minus_2)
                e = utils.getE(word, t)
                prob = 0 if e==0 or q == 0 else np.log2(q) + np.log2(e)
                if prob > p_ti_wi:
                    p_ti_wi = prob
                    tag_i = t
            t_minus_2 = t_minus_1
            t_minus_1 = tag_i
            line_tags.append(tag_i)
        lines_tags.append(line_tags)
    return lines_tags



if __name__ == '__main__':
    input_file_name, q_mle_filename, e_mle_filename, output_file_name, extra_file = sys.argv[1:]
    seperated_lines = utils.seperated_lines_from_file(input_file_name)
    utils.transitions = utils.parse_mle_file(q_mle_filename)
    utils.emissions = utils.parse_mle_file(e_mle_filename)
    utils.tags = utils.get_tags(utils.emissions)
    utils.num_of_words = sum(utils.emissions.values())
    real_tags = utils.extract_tags_from_file('ass1data/data/ass1-tagger-dev')
    best = 0
    # for i in range(1000):
    #     x = np.random.random()
    #     y = np.random.random()
    #     z = np.random.random()
    #     s = x+y+z
    lambda1 = 0.65 #max(x/s,y/s)
    lambda2 = 0.21 #min(x/s,y/s)
    predicted_tags = greedyAlgorithm(seperated_lines, words_possible_tags=utils.get_dict(utils.emissions))
    accuracy = utils.calc_accuracy(predicted_tags, real_tags)
    if accuracy > best:
        best = accuracy
        print(f'lambda1: {lambda1},lambda2: {lambda2},lambda3: {1.0-lambda1-lambda2}')
        print(f"accuracy:  {str(accuracy)}")
