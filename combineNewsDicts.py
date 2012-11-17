import pickle
from datetime import datetime
from datetime import timedelta
from datetime import date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

pkl_file = open('newsDict09.pkl', 'rb')
newsDict09 = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('newsDict10.pkl', 'rb')
newsDict10 = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('newsDict11.pkl', 'rb')
newsDict11 = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('newsDict12.pkl', 'rb')
newsDict12 = pickle.load(pkl_file)
pkl_file.close()

start_date=date(2009, 1, 1)
end_date = date(2012, 11, 17)

combinedNews = dict(newsDict09.items() + newsDict10.items() + newsDict11.items() + newsDict12.items())
totaldays = 0
numStories = 0
combinedNews[date(2009, 12, 31)]=[]
combinedNews[date(2010, 12, 31)]=[]
combinedNews[date(2011, 12, 31)]=[]
for single_date in daterange(start_date, end_date):
	totaldays += 1
	print single_date
	for newsItem in combinedNews[single_date]:
		numStories += 1
		print str(single_date) + newsItem

print "Total number of days: " + str(totaldays)
print "Total number of stories " + str(numStories)
print "Avg stories per day: " + str(numStories/totaldays)

output = open('combinedNewsDictFull.pkl', 'wb')
pickle.dump(combinedNews, output)
output.close()
