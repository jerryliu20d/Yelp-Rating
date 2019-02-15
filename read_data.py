import json as js
from my_deco import timer


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



raw = read_json("./data/review_train.json",1000)