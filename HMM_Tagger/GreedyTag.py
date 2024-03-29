import sys
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
        tag_i, t_minus_1, t_minus_2 = utils.START, utils.START,utils.START
        line_tags = []
        for i, word in enumerate(line):
            if word not in words_possible_tags:
                word = word.lower() if (word.lower() in words_possible_tags) else utils.word_sign(word)
            p_ti_wi = float('-inf')
            for t in sorted(words_possible_tags[word]):
                q = utils.interpulation(t, t_minus_1, t_minus_2)
                e = utils.getE(word, t)
                prob = 0 if e == 0 or q == 0 else np.log2(q) + np.log2(e)
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
    best = 0
    utils.lambda1 = 0.5
    utils.lambda2 = 0.1
    predicted_tags = greedyAlgorithm(seperated_lines, words_possible_tags=utils.get_dict(utils.emissions))
    utils.write_output_file(predicted_tags, seperated_lines, output_file_name)
