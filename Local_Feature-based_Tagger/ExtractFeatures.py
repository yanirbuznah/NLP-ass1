import sys
from collections import Counter

# rarity threshold
import utils

THRESHOLD = 2
# tokens
UNK = '^UNK'
START = '^S^'
END = '^E^'

def get_prefs(wi):
    prefs = {}
    wi_len = len(wi)
    prefs['pref5'] = wi[:5] if wi_len >= 5 else ""
    prefs['pref4'] = wi[:4] if wi_len >= 4 else ""
    prefs['pref3'] = wi[:3] if wi_len >= 3 else ""
    prefs['pref2'] = wi[:2] if wi_len >= 2 else ""
    prefs['pref1'] = wi[0] if wi_len >= 1 else ""
    return prefs


def get_suffs(wi):
    suffs = {}
    wi_len = len(wi)
    suffs['suff5'] = wi[-5:] if wi_len >= 5 else ""
    suffs['suff4'] = wi[-4:] if wi_len >= 4 else ""
    suffs['suff3'] = wi[-3:] if wi_len >= 3 else ""
    suffs['suff2'] = wi[-2:] if wi_len >= 2 else ""
    suffs['suff1'] = wi[-1] if wi_len >= 1 else ""
    return suffs



def extract(sent: list, i, last_two_tags: tuple, rare: bool) -> dict:
    """
    :param sent: sentence as list of words
    :param i: the index of the specific word
    :param last_two_tags: two tags of the words before the specific word
    :param rare: the word rare or not
    :return: features by using extract features similar to the article (https://u.cs.biu.ac.il/~89-680/memm-paper.pdf)
    """
    # featues for all words
    wi = sent[i]
    features = {
        'word_i-1': sent[i - 1] if i > 0 else START,
        'word_i-2': sent[i - 2] if i > 1 else START,
        'word_i+1': sent[i + 1] if len(sent) > i + 1 else END,
        'word_i+2': sent[i + 2] if len(sent) > i + 2 else END,
        'tag_i-1': last_two_tags[0],
        'tag_i-2': last_two_tags[1],
        'form': wi if not rare else utils.word_sign(wi),
        'form_title': wi[:1].upper() + wi[1:].lower(),
        'form_lower': wi.lower(),
    }
    features.update(get_prefs(wi))
    features.update(get_suffs(wi))
    return features


def seperated_lines_from_file(corpus):
    return [line[:-1].split() for line in corpus]


def check_if_word_rare(word):
    return word_counter[word] < THRESHOLD


def extract_all(corpus):
    features = []
    seperated_lines = seperated_lines_from_file(corpus)
    for line in seperated_lines:
        words, tags = zip(*[words.strip().rsplit('/', 1) for words in line])
        tags = (START, START) + tags
        for i in range(len(words)):
            last_two_tags = (tags[i], tags[i - 1])
            rare = check_if_word_rare(words[i])
            f = extract(words, i, last_two_tags, rare)
            features.append((tags[i + 2], f))

    return features


def main():
    global word_counter
    corpus_file, features_file = sys.argv[1:]

    with open(corpus_file, 'r') as f:
        lines = f.readlines()

    words = [pair.rsplit('/', 1)[0] for line in lines for pair in line.strip().split()]
    word_counter = Counter(words)
    all_features = extract_all(lines)

    with open(features_file, 'w') as f:
        for features in all_features:
            f.write(
                f'{features[0]} {" ".join([key + "=" + str(val) for key, val in features[1].items()])}\n'
            )


if __name__ == '__main__':
    main()
