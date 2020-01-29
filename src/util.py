#!/home/knielbo/virtenvs/ndhl/bin/python

import pickle

def load_pcl(fpath):
    with open(fpath, "rb") as fobj:
        mdl = pickle.load(fobj)

    return mdl


def display_topics(model, feature_names, no_top_words=10):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic {}:".format(topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))












if __name__ == "__main__":
    pass