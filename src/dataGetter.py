# dataGetter.py
# William Lyon
# AI Grad Project
# NewzTrader
# dataGetter.py
# 1) Loads pickled news dict
# 2) Downloads historical stock price data
# 3) Joins news dict and stock data in a pandas dataframe
# 4) Set UP/DOWN/NONE classifications for every trading day
# 5) Save news headlines in .CSV files for corpus reader

import pickle
from datetime import datetime
from datetime import timedelta
from datetime import date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

fkl_file = open('combinedNewsDictFull.pkl', 'rb')
news = pickle.load(fkl_file)
fkl_file.close()
start_date=date(2009, 1, 1)
end_date = date(2012, 11, 17)

import pandas as pd
#
from pandas.io.data import DataReader

def only_alphanum(s):
    #s = unicode(s, "utf-8")
    return ' '.join(c for c in s.split() if c.isalnum())
def only_alpha(s):
    return ' '.join(c for c in s.split() if c.isalpha())
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

sp500 = DataReader("^GSPC", "yahoo", datetime(2009, 1, 1))
newsframe = pd.Series(news, name='News')
#descframe = pd.Series(descs, name='Desc')
frameWithNews = sp500.join(pd.DataFrame(newsframe))
#sp500Frame = frameWithNews.join(pd.DataFrame(descframe))
newsframe = pd.Series(news, name='News')
#descframe = pd.Series(descs, name='Desc')
frameWithNews = sp500.join(pd.DataFrame(newsframe))

newsReturns = frameWithNews['Adj Close'].pct_change()
newsReturns.name='Returns'
returnsFrame = frameWithNews.join(pd.DataFrame(newsReturns))

returnsFrame['UP'] = returnsFrame.Returns > 0.01
returnsFrame['DOWN'] = returnsFrame.Returns < -0.01
returnsFrame['NONE'] = (returnsFrame['UP']==False) & (returnsFrame['DOWN']==False)

droppedFrame = returnsFrame

newsUP_frame = droppedFrame[droppedFrame['UP']==True]


newsDOWN_frame = droppedFrame[droppedFrame['DOWN']==True]
newsNONE_frame = droppedFrame[droppedFrame['NONE']==True]

newsNONE_frame = newsNONE_frame.dropna()
newsUP_frame = newsUP_frame.dropna()
newsDOWN_frame = newsDOWN_frame.dropna()

# DO THIS FOR NONE, UP, and DOWN
i = 1
for row in newsNONE_frame.iterrows():
    i+=1
    if len(row[1].ix['News'])>0:
        for line in row[1].ix['News']:
            i+=1
            writeFile = open('%d_news_NONE.csv' % i, 'w')
            writeFile.write(line+'\n')

# DO THIS FOR NONE, UP, and DOWN
i = 1
for row in newsUP_frame.iterrows():
    i+=1
    if len(row[1].ix['News'])>0:
        for line in row[1].ix['News']:
            i+=1
            writeFile = open('%d_news_UP.csv' % i, 'w')
            writeFile.write(line+'\n')

# DO THIS FOR NONE, UP, and DOWN
i = 1
for row in newsDOWN_frame.iterrows():
    i+=1
    if len(row[1].ix['News'])>0:
        for line in row[1].ix['News']:
            i+=1
            writeFile = open('%d_news_DOWN.csv' % i, 'w')
            writeFile.write(line+'\n')

