from lxml import etree
path = '/Users/lyonwj/Documents/CSCI_555/GradProj/pandas/company_news.xml'
doc = etree.parse(path)
root = doc.getroot()
for elt in root.getiterator():
    itemDict[elt.tag]=elt.text
    if elt.tag=='description':
        news.append(itemDict)
        itemDict={}

for dictNews in news:
    i += 1
    print str(i) +':' + dictNews['title'] + ': ' + dictNews['pubDate']