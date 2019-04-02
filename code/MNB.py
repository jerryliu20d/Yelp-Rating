import pandas as pd
raw = pd.read_json("../data/review_train.json", lines=True, chunksize=10000)
raw = raw.__next__()
#%%
# raw['text']
raw = pd.read_json("../data/business_train.json", lines=True, chunksize=10000)
raw = raw.__next__()
#%%
# print(raw['categories'])
# q = raw.categories.value_counts()
cates = list(raw.categories)
cates = [b for b in cates if b]
splited = [b.split(', ') for b in cates]
# np.where(not cates)
#%%
# [[i for i, j in enumerate(c) if j is not None] for c in zip(*cates)]
flat_list = [item for sublist in splited for item in sublist]
df = pd.DataFrame(flat_list)
qq = df[0].value_counts()
