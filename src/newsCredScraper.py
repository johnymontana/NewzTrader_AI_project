
from lxml import etree
from datetime import datetime
from datetime import date
from datetime import timedelta
#import datetime
from dateutil.parser import parse
#import pandas as pd
import pickle
#from pandas.io.data import DataReader
#from pandas.io.data import DataReader
#from pandas.io.data import DataReader

#import pandas as pd
#from datetime import datetime

#iimport pandas as pd
#
#from pandas.io.data import DataReader

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def only_alphanum(s):
    #s = unicode(s, "utf-8")
    return ' '.join(c for c in s.split() if c.isalnum())
def only_alpha(s):
    return ' '.join(c for c in s.split() if c.isalpha())
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

#sp500 = DataReader("SPY", "yahoo", datetime(2009, 1, 1))
news={}
#descs = {}
start_date=date(2011, 7, 27)
end_date = date(2012, 11, 9)
news[date(2009, 11, 9)] = []
news[date(2009, 11, 10)] = []
for single_date in daterange(start_date, end_date):
    news[single_date]=[]
for single_date in daterange(start_date, end_date):
    #print "Starting date: " + str(single_date)
    year = single_date.year
    month = single_date.month
    day = single_date.day
    path = "http://api.newscred.com/articles?access_key=c4bcc3f7c9bf9ec159f51da0a86ca658&sources=104afa30d811d37a5582a39e1662a311&pagesize=99&from_date=%d-%d-%d&to_date=%d-%d-%d 23:59:59" % (year, month, day, year, month, day)
    while True:
        try:
            root = etree.parse(path)
            break
        except etree.XMLSyntaxError:
            pass
    myRoot = root.getroot()

    #news[date(year, month, day)]=[]
    #descs[date(year, month, day)]=[]
    for element in myRoot.iter("article"):
        #for item in element.iter("description"):
         #   desc = item.text
        for item in element.iter("title"):
            title = item.text
        for item in element.iter("created_at"):
            pubDate = parse(item.text)

        news[pubDate.date()].append(only_alphanum(removeNonAscii(title)))
#import pickle
    output = open('newsDict2.pkl', 'wb')
    pickle.dump(news, output)
    output.close()
