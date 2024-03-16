from underthesea import word_tokenize,sent_tokenize
import re, string
import pandas as pd



file_data = open("Data/all_articles.txt","r",encoding='utf-8')
article_text = file_data.read()

def clean_text(text):
    text = re.sub('<.*?>', ' ', text).strip()
    text = text.replace(".", " . ")
    text = re.sub('(\s)+', r'\1', text)
    text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]', ' ', text)
    return text

def normalize_text(text):
    listpunctuation = string.punctuation.replace('_', ' ')
    for i in listpunctuation:
        text = text.replace(i,' ')
    return text.lower()

# list stopwords
filename = './stopwords.csv'
data = pd.read_csv(filename, sep="\t", encoding='utf-8')
list_stopwords = data['stopwords']

def remove_stopword(text):
    pre_text = []
    words = text.split()
    for word in words:
        if word not in list_stopwords:
            pre_text.append(word)
    text2 = ' '.join(pre_text)
    return text2

def sentence_segment(text):

    sents = sent_tokenize(text)
    return sents

def word_segment(sent):
    sent = word_tokenize(sent,format="text")
    return sent

data_save = open('Data/Data.txt','w',encoding='utf-8')
content = clean_text(article_text)
sents = sentence_segment(content)
for sent in sents:
    if(sent != None):
        sent = sent.lower()
        sent = word_segment(sent)
        sent = remove_stopword(normalize_text(sent))
        if(len(sent.split()) > 1):
           data_save.write(sent)
data_save.close()