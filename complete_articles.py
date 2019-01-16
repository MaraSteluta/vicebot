#!/usr/bin/python

import requests
from bs4 import BeautifulSoup as bs

import pymongo
import subprocess

pm = pymongo.MongoClient().vicebot

for i in range(1970 + 1):
    req = requests.get('https://www.vice.com/ro/latest?page=%d' % i)
    soup = bs(req.content, "lxml")
    stop = False

    for large_div in soup.find_all('div', {'class': 'grid__wrapper__card__text'}):
        for title, desc in zip(large_div.find_all('h2', {'class': 'grid__wrapper__card__text__title'}), large_div.find_all('div', {'class': 'grid__wrapper__card__text__summary'})):
            doc = pm.articles.find_one({"_id": title.text})
            if not doc:
                print "Found new article", title.text, desc.text
            else:
                stop = True
            pm.articles.update_one({"_id": title.text}, {"$set": {"desc": desc.text}}, upsert=True)
    if stop:
        break

    print(i)

i = 0
for article in pm.articles.find():
   if i % 5001 == 0:
       print "Loaded article %d, text <%s> desc <%s>" % (i, article['_id'].strip(), article['desc'].strip())
   i += 1

print "Loaded %d articles" % pm.articles.count()
print "Creating markov chain"

subprocess.check_call('python q4grammer.py', shell=True)
