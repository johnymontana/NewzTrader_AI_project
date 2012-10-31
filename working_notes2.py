import nltk as nltk
import os, os.path
path = os.path.expanduser('~/nltk_data')
if not os.path.exists(path):
    os.mkdir(path)
os.path.exists(path)
import nltk.data
path in nltk.data.path
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
reader2 = CategorizedPlaintextCorpusReader('.', r'news_.*\.csv', cat_pattern=r'news_(\w+)\.csv')
reader.categories()
reader.fileids(categories=['UP'])
def bag_of_words(words):
    return dict([(word, True) for word in words])
import collections

def label_feats_from_corpus(corp, feature_detector=bag_of_words):
    label_feats = collections.defaultdict(list)
    for label in corp.categories():
        for fileid in corp.fileids(categories=[label]):
            feats = feature_detector(corp.words(fileids=[fileid]))
            label_feats[label].append(feats)
    return label_feats

def split_label_feats(lfeats, split=0.75):
    train_feats = []
    test_feats = []
    for label, feats in lfeats.iteritems():
        cutoff = int(len(feats) * split)
        train_feats.extend([(feat, label) for feat in feats[:cutoff]])
        test_feats.extend([(feat, label) for feat in feats[cutoff:]])
    return train_feats, test_feats

reader.categories()

lfeats = label_feats_from_corpus(reader2)
lfeats.keys()
train_feats, test_feats = split_label_feats(lfeats)
len(train_feats)
len(test_feats)

from nltk.classify import NaiveBayesClassifier
nb_classifier = NaiveBayesClassifier.train(test_feats)
nb_classifier.labels()

from nltk.classify.util import accuracy
accuracy(nb_classifier, test_feats)

