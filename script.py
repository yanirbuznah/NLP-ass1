import subprocess


#HMM Tagger
subprocess.check_call(["python", "HMM Tagger/MLETrain.py", "ass1data/data/ass1-tagger-train", "q.mle" , "e.mle"])
subprocess.check_call(["python", "HMM Tagger/GreedyTag.py", "ass1data/data/ass1-tagger-dev-input", "q.mle" , "e.mle","output_greedy","ass1data/data/ass1-tagger-dev"])
subprocess.check_call(["python", "HMM Tagger/HMMTag.py", "ass1data/data/ass1-tagger-dev-input", "q.mle" , "e.mle","output_hmm","ass1data/data/ass1-tagger-dev"])

#Local Tagger
subprocess.check_call(["python", "Local Feature-based Tagger/ExtractFeatures.py", "ass1data/data/ass1-tagger-train", "features_file"])
subprocess.check_call(["python", "Local Feature-based Tagger/TrainModel.py", "features_file", "model_file"])
subprocess.check_call(["python", "Local Feature-based Tagger/FeaturesTagger.py", "ass1data/data/ass1-tagger-dev-input", "model_file", "feature_map_file", "output"])
