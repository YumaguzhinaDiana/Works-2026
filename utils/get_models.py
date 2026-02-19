from pickle import load
import os

root = "C:\\Users\\noutb\\PycharmProjects\\commentsToneML\\models\\"
def get_tokenizer():
    tokenizer = None
    try:
        with open(os.path.join(root,'tokenizer1.pkl'), 'rb') as f:
            tokenizer = load(f)

    except Exception as e:
        print(f"Не получилось загрузить модель: {e}")

    return tokenizer


def get_model():
    classifier = None
    try:
        with open(os.path.join(root,'classifier_model1.pkl'), 'rb') as f:
            classifier = load(f)

    except Exception as e:
        print(f"Не получилось загрузить модель: {e}")

    return classifier