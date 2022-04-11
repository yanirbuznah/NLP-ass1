import re
from collections import defaultdict

# rarity threshold
THRESHOLD = 1
# tokens
UNK = '^UNK'
START = '*START*'
END = '*END*'
# interpulation contants
lambda1= 0.6
lambda2 = 0.3


emissions = {}
transitions = {}
tags = {}
num_of_words = 0

def word_sign(word):
    if not re.search(r'\w', word):
        return '^PUNCS'
    elif re.search(r'[A-Z]', word):
        return '^CAPITAL'
    elif re.search(r'\d', word):
        return '^NUM'
    elif re.search(r'(ion\b|ty\b|ics\b|ment\b|ence\b|ance\b|ness\b|ist\b|ism\b)', word):
        return '^NOUNLIKE'
    elif re.search(r'(ate\b|fy\b|ize\b|\ben|\bem)', word):
        return '^VERBLIKE'
    elif re.search(r'(\bun|\bin|ble\b|ry\b|ish\b|ious\b|ical\b|\bnon)', word):
        return '^ADJLIKE'
    elif re.search(r'(ing\b)', word):
        return '^UNK-ing'
    if not word.isalpha():
        return '^UNK-char'
    if word[-2:] == 'ed':
        return '^UNK-ED'
    if word[-2:] == 'ly':
        return '^UNK-LY'
    if word[-1:] == 's':
        return '^UNK-s'
    return UNK



# e(w|t)
def getE(w, t):
    if (w, t) in emissions:
        # P(w|t) = Count(w,t) / Count(t)
        return emissions[(w, t)] / tags[t]
    else:
        return emissions[(UNK, t)] if (UNK, t) in emissions else 0


def interpulation(t3, t2, t1):
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
    d = defaultdict(set)
    mle_sorted = dict(sorted(e_mle.items(), key=lambda item: item[1]))
    for word, tag in reversed(mle_sorted):
        if len(d[word]) < 4:
            d[word].add(tag)
    return d


def parse_mle_file(file):
    mle = {}
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        key, val = line.rsplit("\t",1)
        tags = tuple(key.split())
        mle[tags] = int(val)
    return mle


def lines_from_file(filePath):
    with open(filePath, 'r') as f:
        return f.readlines()


def seperated_lines_from_file(filePath):
    return [line[:-1].split() for line in lines_from_file(filePath)]


def calc_accuracy(predicted_tags, real_tags):
    total = good = 0
    for i, line in enumerate(predicted_tags):
        for j, tag in enumerate(line):
            total += 1
            if tag == real_tags[i][j]:
                good += 1
    return float(good) / total


def extract_tags_from_file(test_file):
    def extract_tags(line):
        return [word_tag.rsplit('/', 1)[-1] for word_tag in line]

    seperated_lines = seperated_lines_from_file(test_file)
    return [extract_tags(line) for line in seperated_lines]


def get_tags(emissions):
    tags = {}
    for e in emissions:
        tags[e[1]] = emissions[e] + tags[e[1]] if e[1] in tags else emissions[e]
    return tags

def write_output_file(predicted_tags, sentences,out_file_name):
    with open(out_file_name, "w") as out_file:
        for sent_idx, line in enumerate(sentences):
            for i, (word, tag) in enumerate(zip(line, predicted_tags[sent_idx])):
                if i + 1 < len(line):
                    out_file.write(f'{word}/{tag} ')
                else:
                    out_file.write(f'{word}/{tag}\n')
