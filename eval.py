import sys
import utils

def eval(pred_file, gold_file):
    real_tags = utils.extract_tags_from_file(gold_file)
    predicted_tags = utils.extract_tags_from_file(pred_file)
    accuracy = utils.calc_accuracy(predicted_tags, real_tags)
    print(f"accuracy:  {str(accuracy)}")

def main():
    pred_file, gold_file = sys.argv[1:]
    eval(pred_file, gold_file)


if __name__ == '__main__':
    main()
