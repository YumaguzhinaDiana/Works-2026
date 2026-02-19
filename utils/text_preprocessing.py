
from nltk.corpus import stopwords
import re
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import pymorphy3
from nltk.tokenize import word_tokenize
import string
from utils.get_models import get_tokenizer

russian_stopwords = stopwords.words("russian")
russian_stopwords.extend(['т.д.', 'т', 'д', 'это','который','свой','своём','всем',"весь"
                          'всё','её','оба','ещё','должный','всякий'])
russian_stopwords = set(russian_stopwords)

tokenizer = get_tokenizer()

max_len = 250


def lemmatization_text(text):
    try:
        morph = pymorphy3.MorphAnalyzer(lang="ru")
        tokens = [token for token in word_tokenize(text)]

        lemmas = []
        for word in tokens:
            parsed = morph.parse(word)
            if parsed and parsed[0].normal_form not in russian_stopwords:
                lemmas.append(parsed[0].normal_form)

        return (
            ' '.join(lemmas)
        )
    except Exception as e:
        print(f"Error: {e} | Text: {text[:50]}")
        return ''


def remove_punctuation(text):
    punct = string.punctuation + '—' + "“" + "”" + "»" + "«" + "\n"
    text = re.sub(r"http\S+", "url", text)
    text = text.replace('ё', 'е')
    text = re.sub('[^a-zA-Zа-яА-Я]+', ' ', text)
    text = re.sub(' +', ' ', text)
    text = text.lower()
    text = re.sub(r"[0-9" + re.escape(punct) + r"]+", " ", text)
    return text.lower()


def token_pad(clean_text: str):
    token_text = tokenizer.texts_to_sequences([clean_text])
    text = pad_sequences(token_text, maxlen=max_len)
    return text



