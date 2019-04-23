"""
Kun Li
This file contains methods to preprocess text corpus and used for created inverted index
"""

from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from collections import defaultdict
import time
import json
import re


class PreProcessing:
    """This class contains the methods to preprocess the text loaded from corpus,
    which is later used for building inverted index.
    """
    def __init__(self):
        self.FREQ_STEMMING = ["film", "direct", "star", "produc", "also"]
        self.PS = PorterStemmer()  # porter stemmer
        self.STOPWORDS = list(stopwords.words("english"))
        self.flatten = lambda t: [x for sub in t for x in self.flatten(sub)] \
            if isinstance(t, list) else [t]  # flatten a nested list (can be useful to deal with some data fields)

    def word_tokenization(self, string):
        """Tokenize the whole string, and return a list of tokens."""
        return word_tokenize(string)

    def token_filter(self, token):
        return re.sub(r'[^a-zA-Z0-9]', '', token)

    def normalize(self, token):
        # remove stopwords and stemming
        token_filtered = self.token_filter(token)
        if token_filtered.lower() in self.STOPWORDS:
            return None
        if token_filtered == "":
            return ""
        elif len(token_filtered) < 2:
            return None
        else:
            stem = self.PS.stem(token_filtered.lower())
            return stem if stem not in self.FREQ_STEMMING else None


    def test_corpus(self, filename="test_corpus.json"):
        """Create a test corpus as a pickle file contains 10 hand-made documents."""
        test_corp = defaultdict(dict)
        titles = ["Movie one the", "Movie two a", "Movie Three an", "Movie Four", "Happy movie five",
                  "romantic movie six", "horror film 7", "movie eight", "Happy film Nine", "Romantic movie Ten"]
        directors = ["Frank", "Tom", "jerry", "terry", "james", "holly", "eros", "jupiter", "marcs", "mao"]
        starrings = ["Frank", "Tom", "jerry", "terry", "james", "holly", "eros", "jupiter", "marcs", "mao"]
        locations = ['USA', 'us', 'America', 'CA', 'UK', 'uk', 'canada', 'china', 'MA', '']
        texts = ["one is a one", "two is a two", "three is a three", "four is a four", "five is a five",
                 "what is a six?",
                 "Here is seven", "no eight", "best is nine", "Ten is the best"]
        # movie free text
        for i, title, director, starring, location, text in zip(range(10), titles, directors, starrings, locations, texts):
            test_corp[str(i)]["title"] = title
            test_corp[str(i)]["director"] = director
            test_corp[str(i)]["starring"] = starring
            test_corp[str(i)]["location"] = location
            test_corp[str(i)]["text"] = text
        json_obj = json.dumps(test_corp)
        with open(filename, 'w') as f:
            f.write(json_obj)
        print ('test corpus has been created!')
