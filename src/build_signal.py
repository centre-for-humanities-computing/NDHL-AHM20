#!/home/knielbo/virtenvs/ndhl/bin/python
"""
Build signal(s) from information dynamics in model

@author: kln@cas.au.dk
"""
import os
import numpy as np
from numpy.matlib import repmat
import scipy as sp
from util import load_pcl

# vis and test
import matplotlib.pyplot as plt


def kld(p, q):
    """ KL-divergence for two probability distributions
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)

    return np.sum(np.where(p != 0, (p-q) * np.log10(p / q), 0))

def jsd(p, q, base=np.e):
    '''Pairwise Jensen-Shannon Divergence for two probability distributions
        - use to avoid division by zero when q = 0    
    '''
    ## convert to np.array
    p, q = np.asarray(p), np.asarray(q)
    ## normalize p, q to probabilities
    p, q = p/p.sum(), q/q.sum()
    m = 1./2*(p + q)
    return sp.stats.entropy(p,m, base=base)/2. +  sp.stats.entropy(q, m, base=base)/2.

def normalize(x, lower=-1, upper=1):
    """ transform x to x_ab in range [a, b]
    """
    x_norm = (upper - lower)*((x - np.min(x)) / (np.max(x) - np.min(x))) + lower
    return x_norm
"""
def build_signals(X, w=3):

    m = len(X)
    # Novelty
    N_hat = np.zeros(m)
    N_sd = np.zeros(m)
    for i, x in enumerate(X):
        submat = X[(i-w):i, ]
        tmp = np.zeros(submat.shape)
        for ii, xx in enumerate(submat):
            tmp[ii] = kld(xx, x)
        N_hat[i] = np.mean(tmp)
        N_sd[i] = np.std(tmp)
    # Transience
    T_hat = np.zeros(m)
    T_sd = np.zeros(m)
    for i, x in enumerate(X):
        submat = X[i:(i+w), ]
        tmp = np.zeros(submat.shape)
        for ii, xx in enumerate(submat):
            tmp[ii] = kld(xx, x)
        T_hat[i] = np.mean(tmp)
        T_sd[i] = np.std(tmp)
    # Resonance
    R = N_hat - T_hat
    R_sd = (N_sd + T_sd)/2

    return [N_hat, N_sd], [T_hat, T_sd], [R, R_sd]
"""

def main():
    bow_mdl = load_pcl(os.path.join("..","mdl","bow_lda.pcl"))
    X = bow_mdl["theta"]
    #fname = os.path.join("..", "dat", "target.pcl")
    #db = load_pcl(fname)
    #content = db["content"]N_hat[i] = np.mean(tmp)
    #metadata = db["metadata"]
    #print(metadata.head(25))

    # ASSERT: X is matrix

    # parameters P of function
    window = 100# abstract time window because the data are not sampled on regular intervals (in sample)
    m = X.shape[0]
    weight = 0.0# parameter to set initial window for novelty and final window for transience
    impute = True
    rescale = True#-1:1 scaling
    
    # ASSERT: win < m
    
    # novelty
    N_hat = np.zeros(m)
    N_sd = np.zeros(m)

    for i, x in enumerate(X):#TODO: remove w+1 limit
        submat = X[(i-window):i,]
        tmp = np.zeros(submat.shape[0])
        if submat.any():
            for ii, xx in enumerate(submat):
                tmp[ii] = jsd(x, xx)
        else:
            tmp = np.zeros([window]) + weight# Comment: set initial windows to 0.0
        
        N_hat[i] = np.mean(tmp)
        N_sd[i] = np.std(tmp)
    #print(N_hat)
    
    # Transience
    T_hat = np.zeros(m)
    T_sd = np.zeros(m)
    
    for i, x in enumerate(X):#TODO: remove w+1 limit
        submat = X[i+1:(i+window+1),]
        tmp = np.zeros(submat.shape[0])
        #print(i, x)
        if submat.any():
            
            for ii, xx in enumerate(submat):
                #print(ii, xx)
                #print(ii, kld(xx,x))         
                tmp[ii] = jsd(x, xx)
                #print(tmp)
            #print("*"*10)
        else:
            tmp = np.zeros([window])
            #print(tmp)
        
        T_hat[i] = np.mean(tmp)
        T_sd[i] = np.std(tmp)
        
    #print(T_hat)
    #T_hat[i] = np.mean(tmp)
    #T_sd[i] = np.std(tmp)
    #print(T_hat)
    #novelty, transience, resonance = build_signals(X, w=w)
    # Resonance
    R = N_hat - T_hat
    R_sd = (N_sd + T_sd)/2
    #print(novelty)
    
    T_hat[-window:] = np.zeros([window]) + weight
    R[:window] = np.zeros([window]) + weight
    R[-window:] = np.zeros([window]) + weight


    if rescale:
        print("rescale initiated")
        R = normalize(R)
        N_hat = normalize(N_hat, lower=0)
        T_hat = normalize(T_hat, lower=0)

    T_hat[-window:] = np.zeros([window]) + weight
    R[:window] = np.zeros([window]) + weight
    R[-window:] = np.zeros([window]) + weight

    if impute:
        print("imputation initiated")

    fig, ax = plt.subplots(1,3,figsize=(15,3))
    ax[0].plot(N_hat,c="k")
    ax[0].axhline(np.mean(N_hat[window:]),c="r",linestyle=":")
    ax[1].plot(T_hat,c="k")
    ax[1].axhline(np.mean(T_hat[:-window]),c="r",linestyle=":")
    ax[2].plot(R,c="k")
    ax[2].axhline(np.mean(R[window:-window]),c="r",linestyle=":")
    ax[2].axhline(0.,c="g",linestyle=":")
    plt.tight_layout()
    plt.savefig("../fig/signal.png")
    plt.close()
if __name__ == "__main__":
    main()




