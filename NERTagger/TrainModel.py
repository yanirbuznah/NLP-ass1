import pickle
import sys
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

words = set()


def read_features_file(features_file):
    tags, features_dict_list = [], []
    with open(features_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        split_line = line.strip().split(' ')
        tag = split_line.pop(0)
        tags.append(tag)
        features_dict = {}
        for feature in split_line:
            key, value = feature.split('=', 1)
            features_dict[key] = value
        words.add(features_dict['form'])
        features_dict_list.append(features_dict)

    return features_dict_list, tags


def make_vectorized_dict(features_file):
    X, y = read_features_file(features_file)
    v = DictVectorizer(sparse=True)
    X = v.fit_transform(X)

    with open('ner.feature_map_file', 'wb') as file:
        pickle.dump(v, file)
        pickle.dump(words, file)
    return X, y


def main():
    features_file, model_file = sys.argv[1:]

    vectorized, tags = make_vectorized_dict(features_file)

    log_reg = LogisticRegression(solver='saga', multi_class='multinomial', random_state=0, max_iter=200, verbose=2,
                                 n_jobs=1, warm_start=True)
    log_reg.fit(vectorized, tags)
    pickle.dump(log_reg, open(model_file, 'wb'))


if __name__ == '__main__':
    main()
