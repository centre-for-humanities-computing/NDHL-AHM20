#!/home/knielbo/virtenvs/ndhl/bin/python
"""
Extract front page material only, clean and normalize
@author: kln@cas.au.dk
"""
import os
import re
import pandas as pd
import pickle
import stanfordnlp
from tqdm import tqdm

def str_cleaner(s):
    s = s[2:-2]# remove start and end tags
    s = re.sub("\d+","",s)
    #s = s.lower()# casefold
    s = re.sub(r"\\n","",s)# remove paragraphs

    return s

def normalize(df, col="paragraphs" ):
    articles = df[col].values
    articles = [str_cleaner(article) for article in articles]
    art_lemma = list()
    nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,pos,lemma',lang="en")
    for text in tqdm(articles):
        doc = nlp(text)
        lemmas = [word.lemma for sent in doc.sentences for word in sent.words]
        art_lemma.append(" ".join(lemmas))
    
    return art_lemma


def main():
    # load data
    metadata = pd.read_csv(os.path.join("..","dat", "metadata.csv"))
    content = pd.read_csv(os.path.join("..","dat", "content.csv"))
    # select meta for frontpage
        # first section
    meta_trgt = metadata.loc[metadata["print_section"] == "A"]
        # first page
    meta_trgt = meta_trgt.loc[meta_trgt["print_page_number"] == 1]
    # select content for frontpage
    cont_trgt = content[content["id"].isin(meta_trgt["id"].values)]
    # reset indices
    meta_trgt = meta_trgt.reset_index(drop=True)
    cont_trgt = cont_trgt.reset_index(drop=True)
    cont_trgt["lemmata"] = normalize(cont_trgt)
    # export
    db_export = dict()
    db_export["content"] = cont_trgt
    db_export["metadata"] = meta_trgt
    #fname = os.path.join("..", "dat", "target.pcl")
    fname = os.path.join("..", "dat", "target_full.pcl")
    with open(fname, "wb") as fobj:
        pickle.dump(db_export, fobj, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()