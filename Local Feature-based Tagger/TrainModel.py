from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
import sys

# TODO: what to do with the tag?

def read_features_file(features_file):
    features_dict_list = []
    with open(features_file,'r') as file:
        lines = file.readlines()
    for line in lines:
        features_dict = {}
        split_line = line.split(' ')
        tag = split_line.pop(0)

        for feature in split_line:
            key, value = feature.split('=')
            features_dict[key] = value
        features_dict_list[(tag, features_dict)]
    return features_dict_list

def make_vectorized_dict(features_file):
    d = read_features_file(features_file)
    v = DictVectorizer(sparse=False)
    v.fit_transform(d)
    return v


def main():
    features_file, model_file = sys.argv[1:]
    vectorized = make_vectorized_dict(features_file)


if __name__ == '__main__':
    main()