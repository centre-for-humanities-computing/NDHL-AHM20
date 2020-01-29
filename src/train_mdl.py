#!/home/knielbo/virtenvs/ndhl/bin/python
"""
train document representation model

@author: kln@cas.au.dk
"""
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import matplotlib as mpl
from util import display_topics, load_pcl

mpl.rcParams.update({"text.usetex": False,
                    "font.family": "serif",
                    "font.serif": "cmr10",
                    "font.weight": "bold",
                    "mathtext.fontset": "cm",
                    "axes.unicode_minus": False
                    })


flatten = lambda l: [item for sublist in l for item in sublist]

def k_grid_search(X, test_size=0.1, gridval=[10, 100, 10], n_iter=10, seed=23):
    X_train, X_test = train_test_split(
        X, test_size=test_size, random_state=seed
        )
    grid = range(gridval[0], gridval[1], gridval[2])
    loglik = list()
    perplex = list()
    for k in grid:
        print("Estimating model at k: {}".format(k))
        lda = LatentDirichletAllocation(
            n_components=k, max_iter=n_iter, learning_method='batch',
            learning_offset=10., random_state=seed, n_jobs=2
            )
        lda.fit(X_train)
        loglik.append(lda.score(X_test))
        perplex.append(lda.perplexity(X_test))
        lda = None
    lda = None

    return list(grid), loglik, perplex

def optimal_k(grid, loglik, perplexity, figname="grid_search.png"):
    y0 = loglik
    ky0 = grid[y0.index(max(y0))]
    y1 = perplexity
    ky1 = grid[y1.index(min(y1))]
    Y = [y0, y1]
    K = [ky0, ky1]
    fig = plt.figure()
    fig, ax = plt.subplots(2, 1)
    for i, y in enumerate(Y):
        ax[i].plot(grid, y, color="k")
        ax[i].axvline(
            K[i], label="$k = {}$".format(K[i]), color="red", linestyle=":"
            )
        ax[i].legend()

    plt.tight_layout()
    plt.savefig(figname)
    plt.close()

    return K


def main():
    fname = os.path.join("..", "dat", "target.pcl")
    db = load_pcl(fname)
    content = db["content"]
    #metadata = db["metadata"]
    lemmata = content["lemmata"].values
    # train vector space
    vectorizer = CountVectorizer(
        analyzer="word", 
        min_df=2,
        max_df=.75,
        max_features=1500,
        stop_words="english",
        ngram_range=(1, 2)
        )
    BoW = vectorizer.fit_transform(lemmata)
    feature_names = vectorizer.get_feature_names()
    

    # set grid size, 
    grid, loglik, perplexity = k_grid_search(
        BoW, test_size=0.25, gridval=[10, 101, 10]
        )
    figname = os.path.join("..", "fig", "grid_search.png")
    K = optimal_k(grid, loglik, perplexity, figname=figname)
    k = K[0]

    print("> Optimal k: {}".format(k))
    n_iter = 10
    lda = LatentDirichletAllocation(
        n_components=k, max_iter=n_iter, learning_method='batch',
        learning_offset=10., random_state=0, n_jobs=2
        )
    lda.fit(BoW)
    theta = lda.fit_transform(BoW)
    phi = lda.components_
    W = np.sum(phi, axis=1)
    out = dict()
    out["bow"] = BoW
    out["vectorizer"] = vectorizer
    out["model"] = lda
    out["theta"] = theta
    out["phi"] = phi
    out["w"] = W
    fname = os.path.join("..", "mdl", "bow_lda.pcl")
    with open(fname, "wb") as fobj:
        pickle.dump(out, fobj, protocol=pickle.HIGHEST_PROTOCOL)

    display_topics(lda, vectorizer.get_feature_names())
    
if __name__ == "__main__":
    main()