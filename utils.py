import re
from collections import defaultdict

# rarity threshold
THRESHOLD = 1
# tokens
UNK = '*UNK*'
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
        return '_PUNCS_'
    elif re.search(r'[A-Z]', word):
        return '_CAPITAL_'
    elif re.search(r'\d', word):
        return '_NUM_'
    elif re.search(r'(ion\b|ty\b|ics\b|ment\b|ence\b|ance\b|ness\b|ist\b|ism\b)', word):
        return '_NOUNLIKE_'
    elif re.search(r'(ate\b|fy\b|ize\b|\ben|\bem)', word):
        return '_VERBLIKE_'
    elif re.search(r'(\bun|\bin|ble\b|ry\b|ish\b|ious\b|ical\b|\bnon)', word):
        return '_ADJLIKE_'
    elif re.search(r'(ing\b)', word):
        return '_UNK_ing_'
    elif len(word) >= 3 and word[-3:-2] == ':':
        return '*UNK-:*'
    if any(x == '-' for x in word):
        return '*UNK--*'
    if not word.isalpha():
        return '*UNK-char*'
    if word[-2:] == 'ed':
        return '*UNK-ED*'
    if word[-3:] == 'ing':
        return '*UNK-ING*'
    if word[-2:] == 'ly':
        return '*UNK-LY*'
    # if word.isupper():
    #     return '*UNK-UPP*'
    if word.istitle():
        return '*UNK-TITLE*'
    # if any(x.isupper() for x in word):
    #     return '*UNK-HAS-UPPER*'
    # if word[-1:] == 's':
    #     return '*UNK-s*'
    # if len(word) < 3:
    #     return '*UNK-SHORT*'
    # else:
    #     return '*UNK-LONG*'
    return UNK

# def word_sign(word):
#
#     # Some general patterns:
#     if re.search(r'^[0-9]+[,/.][0-9]+[,]?[0-9]*$', word) is not None:
#         return 'UNK_NUM'
#     if re.search(r'^[0-9]+:[0-9]+$', word) is not None:
#         return 'UNK_HOUR'
#     if re.search(r'^[0-9]+/[0-9]+-[a-zA-Z]+[-]?[a-zA-Z]*$', word) is not None:
#         return 'UNK_FRUC-WORD'
#     if re.search(r'^[A-Z]+-[A-Z]+$', word) is not None:
#         return 'UNK_AA-AA'
#     if re.search(r'^[a-z]+-[a-z]+$', word) is not None:
#         return 'UNK_aa-aa'
#     if re.search(r'^[A-Z][a-z]+-[A-Z][a-z]+$', word) is not None:
#         return 'UNK_Aa-Aa'
#     if re.search(r'^[A-Z]+$', word) is not None:
#         return 'UNK_UPPER_CASE'
#     if re.search(r'^[A-Z][a-z]+$', word) is not None:
#         return 'UNK_Aa'
#
#     if word[-3:] == 'ing':
#         return 'UNK_ING'
#     if word[-2:] == 'ed':
#         return 'UNK_ED'
#     if word[-3:] == 'ure':
#         return 'UNK_URE'
#     if word[-3:] == 'age':
#         return 'UNK_AGE'
#
#     # Noun Suffixes:
#     if word[-3:] == 'acy':
#         return 'UNK_ACY'
#     if word[-2:] == 'al':
#         return 'UNK_AL'
#     if word[-4:] == 'ance' or word[-4:] == 'ence':
#         return 'UNK_ANCE'
#     if word[-3:] == 'dom':
#         return 'UNK_DOM'
#     if word[-2:] == 'er' or word[-2:] == 'or':
#         return 'UNK_ER'
#     if word[-3:] == 'ism':
#         return 'UNK_ISM'
#     if word[-3:] == 'ist':
#         return 'UNK_IST'
#     if word[-2:] == 'ty' or word[-3:] == 'ity':
#         return 'UNK_TY'
#     if word[-4:] == 'ment':
#         return 'UNK_MENT'
#     if word[-4:] == 'ness':
#         return 'UNK_NESS'
#     if word[-4:] == 'ship':
#         return 'UNK_SHIP'
#     if word[-4:] == 'tion':
#         return 'UNK_TION'
#     if word[-4:] == 'sion':
#         return 'UNK_SION'
#
#     # Verb Suffixes:
#     if word[-3:] == 'ate':
#         return 'UNK_ATE'
#     if word[-2:] == 'en':
#         return 'UNK_EN'
#     if word[-2:] == 'fy':
#         return 'UNK_FY'
#     if word[-3:] == 'ify':
#         return 'UNK_IFY'
#     if word[-3:] == 'ize' or word[-3:] == 'ise':
#         return 'UNK_IZE'
#
#     # Adjective Suffixes:
#     if word[-4:] == 'able' or word[-4:] == 'ible':
#         return 'UNK_ABLE'
#     if word[-2:] == 'al':
#         return 'UNK_AL'
#     if word[-3:] == 'ful':
#         return 'UNK_FUL'
#     if word[-2:] == 'ic' or word[-4:] == 'ical':
#         return 'UNK_IC'
#     if word[-4:] == 'ious' or word[-3:] == 'ous':
#         return 'UNK_OUS'
#     if word[-3:] == 'ish':
#         return 'UNK_ISH'
#     if word[-3:] == 'ive':
#         return 'UNK_IVE'
#     if word[-4:] == 'less':
#         return 'UNK_LESS'
#
#     return 'UNK'


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
    for word, tag in e_mle:
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

