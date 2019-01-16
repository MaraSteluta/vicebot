#!/usr/bin/python

import requests
from bs4 import BeautifulSoup as bs

import pymongo

pm = pymongo.MongoClient().vicebot

for i in range(7278 + 1):
	req = requests.get('https://www.vice.com/en_us/latest?page=%d' % i)
	soup = bs(req.content)

	for large_div in soup.find_all('div', {'class': 'grid__wrapper__card__text'}):
		for title, desc in zip(large_div.find_all('h2', {'class': 'grid__wrapper__card__text__title'}), large_div.find_all('div', {'class': 'grid__wrapper__card__text__summary'})):
			pm.articles_en_us.update_one({"_id": title.text}, {"$set": {"desc": desc.text}}, upsert=True)
	print i, title.text, desc.text

