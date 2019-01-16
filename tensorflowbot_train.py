#!/usr/bin/python3

import pymongo
import yaml
import re
from textgenrnn import textgenrnn

with open("config.yml", "r") as f:
    cfg = yaml.load(f)

textgen = textgenrnn(name='ViceBotRO')

pm = pymongo.MongoClient().vicebot

texts = []
context_labels = []

for article_doc in pm.articles.find({}, {"_id": 1, "desc": 1}):
    text_string = article_doc["_id"].strip().replace(u'\u200b', "")
    texts.append(text_string)
    context_labels.append('vicebot')

    desc_string = article_doc["desc"].strip().replace(u'\u200b', "")
    texts.append(desc_string)
    context_labels.append('vicebot')

for row in open('manual.txt'):
    row = row.strip()
    texts.append(row)
    context_labels.append('vicebot')


if cfg['new_model']:
    textgen.train_new_model(
        texts,
        context_labels=context_labels,
        num_epochs=cfg['num_epochs'],
        gen_epochs=cfg['gen_epochs'],
        batch_size=cfg['batch_size'],
        train_size=cfg['train_size'],
        rnn_layers=cfg['model_config']['rnn_layers'],
        rnn_size=cfg['model_config']['rnn_size'],
        rnn_bidirectional=cfg['model_config']['rnn_bidirectional'],
        max_length=cfg['model_config']['max_length'],
        dim_embeddings=cfg['model_config']['dim_embeddings'],
        word_level=cfg['model_config']['word_level'])
else:
    textgen.train_on_texts(
        texts,
        context_labels=context_labels,
        num_epochs=cfg['num_epochs'],
        gen_epochs=cfg['gen_epochs'],
        train_size=cfg['train_size'],
        batch_size=cfg['batch_size'])
