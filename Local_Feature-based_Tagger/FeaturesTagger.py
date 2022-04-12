import pickle
import sys
from ExtractFeatures import extract
import utils

input_file_name, model_name, feature_map_file, out_file_name = sys.argv[1:]
START_TAG = '^S^'

"""
for efficient computing we predict tags by indexs. (word[0,0],word[1,0]... word[n,0] .... word[0,1],word[1,1]...)
and not for every line (words[0,0],words[0,1]...words[0,n],words[1,0]....words[n,n])

"""

def main():
    #Get information from all the files.
    with open(input_file_name,'r') as fr:
        lines = fr.readlines()

    with open(feature_map_file, 'rb') as f:
        v = pickle.load(f)
        train_words = pickle.load(f)

    log_reg = pickle.load(open(model_name, 'rb'))

    # prepare all sentences and tags for the predictions
    sentences = [l.strip().split() for l in lines]
    num_of_sentences = len(sentences)
    longest_sentence = max([len(s) for s in sentences])
    last_two_tags = [(START_TAG, START_TAG)] * num_of_sentences
    predicted_tags = [[] for _ in range(num_of_sentences)]
    sentences_indexes = list(range(num_of_sentences))

    for i in range(longest_sentence):
        features_i = []

        for sent_idx in sentences_indexes:
            features = extract(sentences[sent_idx], i, last_two_tags[sent_idx], not sentences[sent_idx][i] in train_words)
            features_i.append(features)

        features_i = v.transform(features_i)
        pred_tags = log_reg.predict(features_i)

        for sent_idx, tag in zip(sentences_indexes, pred_tags):
            predicted_tags[sent_idx].append(tag)
            last_two_tags[sent_idx] = (last_two_tags[sent_idx][1], tag)

        indexes_for_removes = [j for j in sentences_indexes if i+1 == len(sentences[j])]
        for j in indexes_for_removes:
            sentences_indexes.remove(j)

    utils.write_output_file(predicted_tags, sentences,out_file_name)



if __name__ == '__main__':
    main()
