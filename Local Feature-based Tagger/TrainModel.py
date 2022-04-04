import pickle

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
import sys

words = set()
# TODO: what to do with the tag?

def read_features_file(features_file):
    # features_file = 'f1'
    tags,features_dict_list = [], []
    with open(features_file,'r') as file:
        lines = file.readlines()
    for line in lines:
        split_line = line.strip().split(' ')
        tag = split_line.pop(0)
        tags.append(tag)
        # features_dict['TAG'] = tag
        features_dict = {}
        for feature in split_line:
            key, value = feature.split('=',1)
            features_dict[key] = value
        words.add(features_dict['form'])
        features_dict_list.append(features_dict)

    return features_dict_list,tags

def make_vectorized_dict(features_file):
    X,y = read_features_file(features_file)
    v = DictVectorizer(sparse=True)
    X = v.fit_transform(X)

    with open('feature_map_file', 'wb') as file:
        pickle.dump(v, file)
        pickle.dump(words, file)
    return X,y


def main():
    features_file, model_file = sys.argv[1:]
    vectorized,tags = make_vectorized_dict(features_file)
    log_reg = LogisticRegression(solver='lbfgs', multi_class='multinomial', penalty='l2', tol=1e-4, random_state=0,
                                 max_iter=1200)
    # sgd = SGDClassifier(max_iter=1200,loss='log')
    # sgd.partial_fit(vectorized,tags,np.unique(tags))
    log_reg.fit(vectorized, tags)

    # Save the trained model to model_file.
    pickle.dump(log_reg, open('model_file', 'wb'))

if __name__ == '__main__':
    main()