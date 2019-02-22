import json as js
from my_decorators.my_deco import timer
import re
from nltk.corpus import stopwords
import nltk
from nltk.stem import PorterStemmer
from autocorrect import spell
import collections
import numpy as np


#%%
@timer
def read_json(file_name, num_lines=-1):
    raw = []
    with open(file_name) as f:
        try:
            while num_lines:
                num_lines = num_lines - 1
                line = f.readline()
                if line:
                    raw.append(js.loads(line))
                else:
                    f.close()
                    break
        except:
            f.close()
    return raw
def redundant(word):
    last_char = ""
    count = 1
    word_list = []
    for char in word:
        if char == last_char:
            count += 1
            if count > 3:
                char = ""
        else:
            count = 1
            last_char = char
        word_list = word_list + list(char)
    return "".join(word_list)
def word_count(raw_text):
    sents = nltk.sent_tokenize(raw_text)
    word = []
    for sent in sents:
        word.append(nltk.word_tokenize(sent))
    # remove punctuation
    pattern = "[\s+.!/_,$%;?,><^*(\"\'~!@#$%^&*(=)_+`-]"
    word = [[re.sub(pattern, "", words) for words in sentences] for sentences in word]
    # remove redundant chars
    word = [[redundant(words) for words in sentences] for sentences in word]
    # remove empty list
    word = [[y for y in x if y] for x in word]
    word = [x for x in word if x]
    # spelling
    word = [list(map(spell, sentences)) for sentences in word]
    # filter stopping words
    filtered_words = [[word for word in sentences if word not in stopwords.words('english')] for sentences in word]
    # remove empty list
    filtered_words = [[y for y in x if y] for x in filtered_words]
    filtered_words = [x for x in filtered_words if x]
    # word stemming
    ps = PorterStemmer()
    stemmed_words = [[ps.stem(word) for word in sentences] for sentences in filtered_words]
    # [print(word) for word in stemmed_words]
    count_list = []
    for sentences in stemmed_words:
        count_dict = collections.defaultdict(int)
        for words in sentences:
            count_dict[words] += 1
        count_list += [count_dict]
    return count_list


#%%
raw = read_json("../data/review_train.json",2000)
count_list = []
y_list = []
for id in range(1600):
    raw_text = raw[id]['text']
    tmp = word_count(raw_text)
    count_list += tmp
    rating = int(raw[id]['stars'])
    y_list += [rating] * len(tmp)
y_mat = np.array(y_list)
#%%
from sklearn.naive_bayes import MultinomialNB
Mnb = MultinomialNB()
# y_pred = gnb.fit()
full_dict = collections.defaultdict(int)
for dictions in count_list:
    for keys in dictions.keys():
        full_dict[keys] = 0
X_mat = np.zeros((len(count_list), full_dict.__len__()),np.int8)
for id in range(len(count_list)):
    tmp = full_dict.copy()
    tmp.update(count_list[id])
    X_mat[id] = list(tmp.values())
pred = Mnb.fit(X=X_mat, y=y_mat).predict(X_mat)
print(np.sqrt(np.mean(np.power(pred-y_mat, 2))))
#%% test
test_list = []
y_test = []
for id in np.linspace(1601, 2000, 400, dtype=np.int16):
    raw_text = raw[id]['text']
    tmp = word_count(raw_text)
    test_list += tmp
    rating = int(raw[id]['stars'])
    y_test += [rating] * len(tmp)
y_test = np.array(y_test)
#%%
x_test = np.zeros((len(y_test), X_mat.shape[1]), dtype=np.int16)
for words_id in range(len(list(full_dict.keys()))):
    for sentences_id in range(len(y_test)):
        x_test[sentences_id, words_id] = test_list[sentences_id][list(full_dict.keys())[words_id]]
#%%
model = Mnb.fit(X=X_mat, y=y_mat)
pred_test = model.predict(x_test)
print(np.sqrt(np.mean(np.power(pred_test-y_test, 2))))
