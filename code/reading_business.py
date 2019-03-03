    import pandas as pd
    import numpy as np
    from itertools import chain
    # from my_decorators import my_deco
    #%%
    js_reader = pd.read_json("../data/business_train.json", orient="recoreds", lines=True, chunksize=20000)
    raw = js_reader.__next__()
    #%%


    # @my_deco.timer1
    def cate_split(df):
        def chainer(series):
            # return list(chain.from_iterable(list(map(lambda x: x.split(', '), [x for x in series if x]))))
            return list(chain.from_iterable(list(map(lambda x: x.split(', ') if x else [x], series))))

        len_series = raw['categories'].str.split(', ').map(lambda x: len(x) if x else 1)
        df = pd.DataFrame({'attributes': np.repeat(df['attributes'], len_series),
                           'business_id': np.repeat(df['business_id'], len_series),
                           'categories': chainer(df['categories']),
                           'city': np.repeat(df['city'], len_series),
                           'hours': np.repeat(df['hours'], len_series),
                           'is_open': np.repeat(df['is_open'], len_series),
                           'latitude': np.repeat(df['latitude'], len_series),
                           'longitude': np.repeat(df['longitude'], len_series),
                           'name': np.repeat(df['name'], len_series),
                           'postal_code': np.repeat(df['postal_code'], len_series),
                           'state': np.repeat(df['state'], len_series),
                           })

        return df
    #%%
    new_raw = cate_split(raw)
    #%%
    len(set(new_raw['categories']))  # total number of categories
    # all_cate = sorted(set(new_raw['categories']), key=lambda k: (k is None, k))
    new_raw.groupby("categories").size()["Chinese"]
    chinese = new_raw.iloc[np.where(new_raw["categories"] == "Chinese")[0], :]
    #%%
    # set(map(lambda x: x.keys, chinese['attributes']))
    attr = chinese['attributes']
