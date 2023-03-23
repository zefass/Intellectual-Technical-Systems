import string
import re
from scipy import spatial
from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import numpy as np
import json


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def read_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = json.load(f)
    return text

def word_freq(filenm):
    text = read_file(filenm)
    text_nopunct = "".join([char.lower() for char in text if char not in string.punctuation])
    text_onestring = re.sub('\n', ' ', text_nopunct) #делает текст в одну строку
    tokens = word_tokenize(text_onestring, language="russian")
    fdist = FreqDist(tokens) #Соответствие слов и частоты их появления
    top_words = fdist.most_common() #Отсортированный список от самого частого слова к самому редкому
    return top_words

def text_edit(text):
    text_nonum = re.sub(r'\d+', '', text) #Удаляет числа
    text_noeng = re.sub(r'[a-zA-Z]', '', text_nonum)  # Удаляет английский текст
    text_nopunct = "".join([char.lower() for char in text_noeng if char not in string.punctuation]) #удаляет пунктуацию и заменяет заглавные буквы строчными
    text_tokens = word_tokenize(text_nopunct) #Делит текст на токены - отдельные слова
    text_tokenize = [word for word in text_tokens if not word in stopwords.words('russian')] #удаляет стоп-слова
    return text_tokenize

model = KeyedVectors.load_word2vec_format('./ruwiki_20180420_100d.txt', binary=False)
index2word_set = set(model.index_to_key)

def avg_feature_vector(text, model, num_features, index2word_set):
    Vec = np.zeros((num_features,), dtype='float32')
    total_words = 0
    for word in text:
        if word in index2word_set:
            total_words += 1
            Vec = np.add(Vec, model[word])
    Vec = np.divide(Vec, total_words)
    return Vec


def find_similar(text, model):
    sentence1vector = avg_feature_vector(
        text_edit(text), model=model, num_features=100, index2word_set=index2word_set)
    dists = []
    for i, value in enumerate(read_json('books.json')['collections']):
        sentence2vector = avg_feature_vector(
            text_edit(value['text']), model=model, num_features=100, index2word_set=index2word_set)
        sim = spatial.distance.cosine(sentence1vector, sentence2vector)
        dists.append(sim, value['type'])
    min_dist, min_text = min(dists, key=lambda x: x[0])
    print(min_text)

find_similar("file.txt", model=model)
print(word_freq("file.txt"))
