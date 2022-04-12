import subprocess

pred_gold_files = [
                    ('POS greedy', 'hmm-greedy-predictions.txt','ass1data/data/ass1-tagger-dev'),
                    ('POS viterbi', 'hmm-viterbi-predictions.txt','ass1data/data/ass1-tagger-dev'),
                    ('POS features', 'feats-predications.txt','ass1data/data/ass1-tagger-dev'),
                    ('NER viterbi', 'ner/dev', 'ner.hmm.pred'),
                    ('NER features', 'ner/dev', 'ner.feats.pred'),
]

#HMM Tagger
# subprocess.check_call(["python", "HMM_Tagger/MLETrain.py", "ass1data/data/ass1-tagger-train", "q.mle" , "e.mle"])
# subprocess.check_call(["python", "HMM_Tagger/GreedyTag.py", "ass1data/data/ass1-tagger-dev-input", "q.mle" , "e.mle","hmm-greedy-predictions.txt","ass1data/data/ass1-tagger-dev"])
# subprocess.check_call(["python", "HMM_Tagger/HMMTag.py", "ass1data/data/ass1-tagger-dev-input", "q.mle" , "e.mle","hmm-viterbi-predictions.txt","ass1data/data/ass1-tagger-dev"])

# #Local Tagger
# subprocess.check_call(["python", "Local_Feature-based_Tagger/ExtractFeatures.py", "ass1data/data/ass1-tagger-train", "fetures_file"])
# subprocess.check_call(["python", "Local_Feature-based_Tagger/TrainModel.py", "fetures_file", "model_file"])
# subprocess.check_call(["python", "Local_Feature-based_Tagger/FeaturesTagger.py", "ass1data/data/ass1-tagger-dev-input", "model_file", "feature_map_file", "feats-predications.txt"])

#NER Tagger
# subprocess.check_call(["python", "HMM_Tagger/MLETrain.py", "ner/train", "ner.q.mle" , "ner.e.mle"])
# subprocess.check_call(["python", "HMM_Tagger/HMMTag.py", "ner/dev-input", "ner.q.mle", "ner.e.mle", "ner.hmm.pred", "extra_file"])
# subprocess.check_call(["python", "Local_Feature-based_Tagger/ExtractFeatures.py", "ner/train", "ner.fetures_file"])
# subprocess.check_call(["python", "Local_Feature-based_Tagger/TrainModel.py", "ner.fetures_file", "ner.model_file"])
# subprocess.check_call(["python", "Local_Feature-based_Tagger/FeaturesTagger.py", "ner/dev-input", "ner.model_file", "ner.feature_map_file", "ner.feats.pred"])

#Check outputs
# for test_name,pred_file,gold_file in pred_gold_files:
#     print(f"Testing {test_name}...")
#     subprocess.check_call(["python", "eval.py", f"{pred_file}", f"{gold_file}"])
#     print('------------------------')

#Check span acc for ner
print("Testing NER viterbi (span)")
subprocess.check_call(["python", "NERTagger/NER_eval.py", "ner/dev" ,"ner.hmm.pred"])
print('------------------------')

print("Testing NER features (span)")
subprocess.check_call(["python", "NERTagger/NER_eval.py", "ner/dev" ,"ner.feats.pred"])
print('------------------------')
