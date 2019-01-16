import random
import pymongo
from collections import defaultdict

d = defaultdict(lambda: set([]))

# collection to use
col = pymongo.MongoClient().vicebot.articles
#col = pymongo.MongoClient().vicebot.articles_en_us

startwords = set([])


# Size of markov chain context size
#L = 3
L = 4
#L = 5


def process_text(text_string, startwords, d):
	words2 = []
	for word in text_string.split():
		try:
			words2.append(word.decode('utf8'))
		except:
			words2.append(word)

	text = ["STARTWORD"] + words2 + ["STOPWORD"]

	startwords.add(tuple(text[0:L-1]))

	for ARR in zip(*(text[i:] for i in range(L))):
		d[tuple(ARR[0:L-1])].add(tuple(ARR[1:L]))


for article_doc in col.find({}, {"_id": 1, "desc": 1}):
	text_string = article_doc["_id"].strip().replace(u'\u200b', "")
	process_text(text_string, startwords, d)

	desc_string = article_doc["desc"].strip().replace(u'\u200b', "")
	process_text(desc_string, startwords, d)

while True:
	myr1 = random
	myr2 = random
	scores = []

	CHAIN = myr1.choice(list(startwords))

	sentence = []
	while CHAIN[-1] != "STOPWORD":
		sentence.append(CHAIN[1])
		scores.append(len(d[tuple(CHAIN)]))
		CHAIN = myr2.choice(list(d[tuple(CHAIN)]))

	for i in range(1, L-2):
		sentence.append(CHAIN[i])

	if sum(scores) / float(len(scores)) >= 2.000000001:
		print u" ".join(sentence), sum(scores) / float(len(scores))
		raw_input('>>> ')
