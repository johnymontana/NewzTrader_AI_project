# nbTrainer.py
# William Lyon
# AI Grad Project
# NewzTrader
# nbTrainer.py
#  1) Load NLTK corpus reader for naive bayes classifier
#  2) Train NB classifier with random 90% of corpus features
#  3) Test NB classifier with remaining 10% of corpus features and report
#  accuracy
#  TODO: recall, precision reports; improve classifier (only strong words?)

# NLTK - train nb_classifier


import random
import nltk as nltk
#nltk.download()
from nltk.corpus import stopwords
import os, os.path
path = os.path.expanduser('~/nltk_data')
if not os.path.exists(path):
    os.mkdir(path)
os.path.exists(path)
import nltk.data
path in nltk.data.path
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
reader = CategorizedPlaintextCorpusReader('.', r'.*_news_.*\.csv', cat_pattern=r'.*_news_(\w+)\.csv')
reader.categories()

def bag_of_words(words):
    return dict([(word, True) for word in words if word[0].isalpha()])
import collections
def bag_of_words_not_in_set(words, badwords):
    return bag_of_words(set(words)-set(badwords))

def bag_of_non_stopwords(words, stopfile='english'):
    badwords = stopwords.words(stopfile)
    return bag_of_words_not_in_set(words, badwords)

from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder

def bag_of_bigrams_words(words, score_fn=BigramAssocMeasures.chi_sq, n=2000):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    dictOfBigrams = bag_of_words(bigrams)
    dictOfBigrams.update(bag_of_non_stopwords(words))
    return dictOfBigrams

def label_feats_from_corpus(corp, feature_detector=bag_of_bigrams_words):
    label_feats = collections.defaultdict(list)
    for label in corp.categories():
        for fileid in corp.fileids(categories=[label]):
            feats = feature_detector(corp.words(fileids=[fileid]))
            label_feats[label].append(feats)
    return label_feats

def split_label_feats(lfeats, split=0.90):
    train_feats = []
    test_feats = []
    for label, feats in lfeats.iteritems():
        random.shuffle(feats, random.random)
        cutoff = int(len(feats) * split)
        train_feats.extend([(feat, label) for feat in feats[:cutoff]])
        test_feats.extend([(feat, label) for feat in feats[cutoff:]])
    return train_feats, test_feats




reader.categories()

lfeats = label_feats_from_corpus(reader)
lfeats.keys()
train_feats, test_feats = split_label_feats(lfeats)
len(train_feats)
len(test_feats)

from nltk.classify import NaiveBayesClassifier
nb_classifier = NaiveBayesClassifier.train(train_feats)
nb_classifier.labels()

from nltk.classify.util import accuracy
accuracy(nb_classifier, test_feats)


