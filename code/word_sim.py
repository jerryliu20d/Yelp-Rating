import string
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn import metrics, model_selection

texts = pd.DataFrame.from_csv("chinese_review.csv")
texts = texts.text[1:1000]

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

import gensim
word_set = set([x for y in X_train_review for x in y])

model = gensim.models.Word2Vec(sentences=X_train_review, size=len(word_set), window=5, min_count=1, workers=2, sg=1)
# model.save("word2vec.model")
#%%
model.wv.most_similar_cosmul(positive=["like", "eat"])
print(model.predict_output_word(["rice"], topn=60))
#%%
with open("time.txt") as f:
    food_words = f.readlines()[0].split(',')
food_words = list(set(food_words))
#%%
predict = model.predict_output_word(food_words, topn=100)

#%%
with open("clean.txt", 'w') as f:
    for line in sorted(predict, key=lambda x: x[1], reverse=True):
        f.write(line[0])
        f.write(",")
#%%
file_name = 'time.txt'
with open(file_name) as f:
    food_words = f.readlines()[0].split(',')
food_words = list(set(food_words))
with open(file_name, 'w') as f:
    for line in food_words:
        f.write(line)
        f.write(",")
#%%
def run_lgb(train_X, train_y, val_X, val_y, test_X):
    params = {
        "objective": "regression",
        "metric": "rmse",
        "num_leaves": 30,
        "min_child_weight": 50,
        "learning_rate": 0.05,
        "bagging_fraction": 0.7,
        "feature_fraction": 0.7,
        "bagging_frequency": 5,
        "bagging_seed": 2018,
        "verbosity": -1
    }

    lgtrain = lgb.Dataset(train_X, label=train_y)
    lgval = lgb.Dataset(val_X, label=val_y)
    evals_result = {}
    model = lgb.train(params, lgtrain, 1000, valid_sets=[lgval], early_stopping_rounds=100, verbose_eval=100,
                      evals_result=evals_result)

    pred_test_y = model.predict(test_X, num_iteration=model.best_iteration)
    return pred_test_y, model, evals_result


train_X = aa
test_X = aa[0:5]
train_y = y

pred_test = 0
kf = model_selection.KFold(n_splits=5, random_state=2018, shuffle=True)
for dev_index, val_index in kf.split(train_X):
    dev_X, val_X = train_X.loc[dev_index, :], train_X.loc[val_index, :]
    dev_y, val_y = train_y[dev_index], train_y[val_index]

    pred_test_tmp, model, evals_result = run_lgb(dev_X, dev_y, val_X, val_y, test_X)
    pred_test += pred_test_tmp
pred_test /= 5.

fig, ax = plt.subplots(figsize=(12,10))
lgb.plot_importance(model, max_num_features=50, height=0.8, ax=ax)
ax.grid(False)
plt.title("LightGBM - Feature Importance", fontsize=15)
plt.show()