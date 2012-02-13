#!/usr/bin/python 
#
# wget wget http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
# unzip imm6010.zip

import math
import re
import sys
from pymongo import Connection
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

#Open a connection to MongoDb (localhost)
connection =  Connection()
db = connection.tweets

# word list is as of December 2011 
filenameWords = 'words/wordweightings.txt'
wordlist = dict(map(lambda (w, s): (w, int(s)), [
            ws.strip().split('\t') for ws in open(filenameWords) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    words = pattern_split.split(text.lower())
    sentiments = map(lambda word: wordlist.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
    else:
        sentiment = 0
    return sentiment



if __name__ == '__main__':
    # Get the records from Mongo
    records = db.tweets.find()
    sentiments = map(sentiment, [ tweet['text'] for tweet in records ])
    db.sentiment.insert({'sentiment': "%6.2f" % (sum(sentiments)/math.sqrt(len(sentiments))), 'date': datetime.datetime.utcnow()})
    print("%6.2f" % (sum(sentiments)/math.sqrt(len(sentiments))))

