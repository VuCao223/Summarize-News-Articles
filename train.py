import os
import pandas as pd
import string
from pyvi import ViTokenizer
from gensim.models import Word2Vec,FastText

# path data
pathdata = 'document/all_articles.txt'

def read_data(path):
    traindata = []
    sents = open(pathdata, 'r',encoding="utf-8").readlines()
    for sent in sents:
        traindata.append(sent.split())
    return traindata


if __name__ == '__main__':
    train_data = read_data(pathdata)
    model = Word2Vec(train_data, vector_size=500, window=20, min_count=5, workers=2, sg=0)
    model.save("model/word2vec_3.model")
    # model_fasttext = FastText(size=300, window=10, min_count=2, workers=4, sg=1)
    # model_fasttext.build_vocab(train_data)
    # model_fasttext.train(train_data, total_examples=model_fasttext.corpus_count, epochs=model_fasttext.iter)
    # model_fasttext.wv.save("model/fasttext.model")