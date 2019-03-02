import nltk
import pandas as pd
import string
import re
import numpy as np
# import autocorrect
# from my_decorators.my_deco import timer


#%%
# @timer
def all_clean(all_info):
    reviews = list(map(review_clean, all_info))
    n_reviews = list(map(len, reviews))
    reviews = pd.DataFrame([x for y in reviews for x in y], columns=["bussiness_id", "stars", "text", "date"])
    tmp_mat = np.transpose([range(len(all_info)), n_reviews])
    uid = [[x[0]]*x[1] for x in tmp_mat]  # create uid for each customer
    uid = [y for x in uid for y in x]  # flatten the nested list
    reviews['uid'] = uid
    return reviews


def review_clean(info):
    def word_clean(word):
        word = re.sub(r'(.)\1{3,}', r'\1\1\1', word)
        # word = autocorrect.spell(word)
        word = cList.get(word, word.lower())
        word = list(map(lambda word: '' if word in stopwords else word, word.split()))
        word = ' '.join(list(map(ps.stem, word)))
        return word
    sentences = nltk.sent_tokenize(info['text'])
    # remove punctuation
    nopunc = [''.join([char for char in sent if char not in string.punctuation]) for sent in sentences]
    # remove repeated chars
    ps = nltk.stem.PorterStemmer()
    cleand_review = [' '.join(list(map(word_clean, sentences.split()))) for sentences in nopunc]
    return list(map(lambda x:  [info["business_id"], info["stars"]] + [x] + [info["date"]], list(map(lambda sentence: ' '.join(sentence.split()), cleand_review))))


#%%
chunksize = 20
js_reader = pd.read_json("C:/Doc/19spring/STAT628/Module2/Module2/data/review_train.json", lines=True, chunksize=chunksize, orient="records", typ="series")
while True:
    try:
        raw = js_reader.__next__()
        cList = pd.read_json("correct_corpus.json", typ='series')
        cList.to_dict()
        with open("stopwords.txt") as f:
            stopwords = f.readlines()[0].split(',')
        count = 1
        review_cleaned = all_clean(raw)
        if count != 1:
            review_cleaned.to_csv('cleaned_review.csv', header=False, index=False, mode='a', line_terminator="")
        else:
            review_cleaned.to_csv('cleaned_review.csv', header=True, index=False)
    except StopIteration:
        print("No more data")


