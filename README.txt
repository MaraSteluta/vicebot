fill_up_initial_articles_ro.py
Refills up all the articles titles and descriptions from Vice Romania.
A dump of that collection is provided in articles.json

fill_up_initial_articles_en.py
Refills up all the articles titles and descriptions from Vice Romania.
A dump of that collection is provided in fill_up_initial_articles_en.py

complete_articles.py
Tries to refill missing articles and runs q4grammer.py

q4grammer.py
Creates a markov chain and does random walks.
You can switch the collection from romanian to english. col=..
You can play with the length of the context from L=3,4,5.
4 works best, but you can find some gems with 3 as well.
