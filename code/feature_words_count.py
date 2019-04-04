import string
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn import metrics, model_selection

texts = pd.DataFrame.from_csv("chinese_review.csv")
# raw = texts
# texts = texts.text
raw2 = raw.iloc[[x for x in range(len(raw)) if raw.iloc[x]['business_id']==9853]]
#%%
raw3 = raw2.iloc[[x for x in range(len(raw2)) if raw2.iloc[x].stars <= 3]]
texts = raw3.text

with open("stopwords.txt") as f:
    stop_words = f.readlines()[0].split(',')
X_train_review = []
for line in texts:
    tokens = word_tokenize(line)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    words = [w for w in words if w not in stop_words]
    X_train_review.append(words)
#%%
with open("clean.txt") as f:
    clean_word = f.readlines()[0].split(',')
with open("food.txt") as f:
    food_word = f.readlines()[0].split(',')
with open("price.txt") as f:
    price_word = f.readlines()[0].split(',')
with open("service.txt") as f:
    service_word = f.readlines()[0].split(',')
with open("time.txt") as f:
    time_word = f.readlines()[0].split(',')
#%%
def count_words(review_list, bags):
    return [sum([x.count(y) for y in bags]) for x in review_list]
raw['clean'] = count_words(X_train_review, clean_word)
raw['food'] = count_words(X_train_review, food_word)
raw['price'] = count_words(X_train_review, price_word)
raw['service'] = count_words(X_train_review, service_word)
raw['time'] = count_words(X_train_review, time_word)
#%%
raw['word_len'] = [len(x) for x in X_train_review]
#%%
raw.to_csv("chinese_count.csv")
import pickle
with open("word_lists.pkl", 'wb') as f:
    pickle.dump(X_train_review, f)
#%%
#%%
rv = raw2['text']
#%%
dd= [sum([x.count(y) for y in price_word]) for x in X_train_review]
#%%
m = sorted(dd, reverse=True)[0:10]
ind = [i for i, j in enumerate(dd) if j in m]
[raw3.iloc[x].text for x in ind]
