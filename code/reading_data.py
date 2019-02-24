import nltk
import pandas as pd
import string
import re
# import autocorrect
# from my_decorators.my_deco import timer


#%%
# @timer
def all_clean(review):
    return list(map(review_clean, review))


def review_clean(review):
    def word_clean(word):
        word = re.sub(r'(.)\1{3,}', r'\1\1\1', word)
        # word = autocorrect.spell(word)
        word = cList.get(word, word.lower())
        word = list(map(lambda word: '' if word in stopwords else word, word.split()))
        word = ' '.join(list(map(ps.stem, word)))
        return word

    sentences = nltk.sent_tokenize(review)
    # remove punctuation
    nopunc = [''.join([char for char in sent if char not in string.punctuation]) for sent in sentences]
    # remove repeated chars
    ps = nltk.stem.PorterStemmer()
    cleand_review = [' '.join(list(map(word_clean, sentences.split()))) for sentences in nopunc]
    return list(map(lambda sentence: ' '.join(sentence.split()), cleand_review))


#%%
raw = pd.read_json("C:/Doc/19spring/STAT628/Module2/Module2/data/review_train.json", lines=True, chunksize=20000, orient="columns")
raw = raw.__next__()
cList = pd.read_json("correct_corpus.json", typ='series')
cList.to_dict()
with open("stopwords.txt") as f:
    stopwords = f.readlines()[0].split(',')
review_cleaned = all_clean(raw['text'][0:100])
