#!/home/knielbo/virtenvs/ndhl/bin/python
"""

@author: kln@cas.au.dk
"""
import os
import pandas as pd

def main():
    DATPATH = os.path.join("..","dat")
    data_cls = ["content", "metadata"]
    DATA = dict()
    for cls in data_cls:
        DATA[cls] = pd.read_csv(os.path.join(DATPATH, cls+".csv"))
        print(DATA[cls].shape)



if __name__ == "__main__":
    main()