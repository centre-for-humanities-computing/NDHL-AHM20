#!/home/knielbo/virtenvs/ndhl/bin/python
"""
Describe feature distributions of (meta)data
@author: kln@cas.au.dk
"""
import os
import matplotlib.pyplot as plt
from util import load_pcl
from datetime import datetime


def main():
    fname = os.path.join("..", "dat", "target.pcl")
    db = load_pcl(fname)
    metadata = db["metadata"]

    print("#"*100, file=open("output.txt", "a"))
    print(datetime.now(), file=open("output.txt", "a"))
    print(metadata.corr(), file=open("output.txt", "a"))
    print("\n\n",file=open("output.txt", "a"))
    print(metadata.describe(), file=open("output.txt", "a"))
    
    for i, col in enumerate(metadata):
        bins = len(list(set(metadata[col].values)))
        metadata[col].hist(bins=bins,color="k")
        plt.title(col)
        plt.savefig(os.path.join("..","fig","DIST_{}.png".format(col)))
        plt.close()

if __name__ == "__main__":
    main()