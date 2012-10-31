import pandas as pd
from datetime import datetime
from pandas.io.data import DataReader

pd.set_printoptions(max_rows=2000)


aapl = DataReader("AAPL", "yahoo", datetime(2010, 1, 1), datetime(2012, 10, 30))
returns = aapl.pct_change()

def f(x):
    if x > 0.01:
        return 1
    elif x < -0.01:
        return -1
    else:
        return 0

frame = returns.applymap(f)

frame['UP'] = frame['Adj Close'] == 1
frame['DOWN'] = frame['Adj Close'] == -1
frame['NONE'] = frame['Adj Close'] ==0

from lxml import etree
import datetime
from dateutil.parser import parse
path = "http://www.google.com/finance/company_news?q=NASDAQ:AAPL&output=rss&num=500"
root = etree.parse(path)
myRoot = root.getroot()
news={}
for element in myRoot.iter("item"):
    for item in element.iter("pubDate"):
        pubDate = parse(item.text)
    for item in element.iter("title"):
        title = item.text
    news[pubDate.date()]=title

newsframe = pd.Series(news)
frameWithNews = frame.join(pd.DataFrame(newsframe))
newsUP = frameWithNews['UP'==True]
newsDOWN = frameWithNews['DOWN'==True]
newsNONE = frameWithNews['NONE' == True]

import pandas.io as io

newsUP.dropna().to_csv('newsUP.csv')
newsDOWN.dropna().to_csv('newsDOWN.csv')
newsNONE.dropna().to_csv('newsNONE.csv')





