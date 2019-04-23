"""
Author: Kun Li
This file create various inverted index and store them in shelve
"""

import shelve
import json
from preprocessing import PreProcessing
import time
prepro = PreProcessing()


def timing(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print ("Time it took to build this index: " + str((t2 - t1)) + "\n")
    return wrapper


@timing
def title_text_inverted_index(shelvename1, shelvename2, corpus_name='2018_movies.json'):
    """Create an inverted index over terms in "title" and "text" fields"""
    with open(corpus_name) as f:
        corpus = json.load(f)
    id = sorted(corpus.keys(), key=lambda d: int(d))
    for i, key in enumerate(id):
        if i < 800:
            # there are too many terms, so we have to store them as two seperate shelve
            shelve_file = shelve.open(shelvename1, writeback=False)
        else:
            shelve_file = shelve.open(shelvename2, writeback=False)
        title = corpus[key]["Title"]
        title = " ".join(title)
        text = corpus[key]["Text"]
        tokens = prepro.word_tokenization(title + ' ' + text)
        terms = set(prepro.normalize(token) for token in tokens)
        terms -= {None, ""}
        # all terms from one document
        for term in terms:
            try:
                if term not in shelve_file:
                    shelve_file[term] = [key]
                else:
                    try:
                        temp = shelve_file[term]
                    except KeyError:
                        print('key error: ' + term)
                        continue
                    else:
                        temp.append(key)
                        shelve_file[term] = temp
            except UnicodeEncodeError:
                print('unicode error: ' + term)
                continue
        shelve_file.close()
    print("main inverted index created!")


@timing
def director_starring_location_inverted_index(shelvename, field, corpus_name="2018_movies.json"):
    """Create inverted index for director, starring and location."""
    with open(corpus_name) as f:
        corpus = json.load(f)
    inverted_shelve = shelve.open(shelvename, writeback=False)
    id = sorted(corpus.keys(), key=lambda d: int(d))
    for key in id:
        field_value = corpus[key][field]
        content = prepro.flatten(field_value)
        tokens = prepro.word_tokenization(' '.join(content))
        terms = set(prepro.normalize(token) for token in tokens)
        terms -= {None, ""}
        for term in terms:
            try:
                if term not in inverted_shelve:
                    inverted_shelve[term] = [key]
                else:
                    try:
                        temp = inverted_shelve[term]
                    except KeyError:
                        print("key error: " + term)
                        continue
                    else:
                        temp.append(key)
                        inverted_shelve[term] = temp
            except UnicodeEncodeError:
                print("unicode error: " + term)
                continue
    inverted_shelve.close()
    print(field + " inverted index created!")


@timing
def all_doc_shelve(filename, shelvename="all_doc_shelve"):
    """Get all the document data and store it in a shelve."""
    with open(filename, 'rb') as f:
        corpus = json.load(f)
    all_doc_shelve = shelve.open(shelvename, writeback=False)
    for id in corpus.keys():
        starring = prepro.flatten(corpus[id]['Starring'])
        all_doc_shelve[id] = {"Title": corpus[id]["Title"],
                              "Starring": ', '.join(starring),
                              "Director": corpus[id]["Director"],
                              "Location": corpus[id]["Location"],
                              "Text": corpus[id]["Text"]}
    print("all_doc_shelve created")


def intersection(posting_list):
    if not posting_list:
        return []
    elif len(posting_list) == 1:
        return posting_list[0]
    result = []
    i, j = 0, 0
    while i < len(posting_list[0]) and j < len(posting_list[1]):
        if int(posting_list[0][i]) > int(posting_list[1][j]):
            j += 1
        elif int(posting_list[0][i]) < int(posting_list[1][j]):
            i += 1
        else:
            result.append(posting_list[0][i])
            i += 1
            j += 1
    posting_list.insert(0, result)
    # intersect recursively
    return intersection(posting_list)


def conjunctive_query(token_list, shelve):
    stopwords = []
    unknown = []
    terms = []
    for token in token_list:
        normalized = prepro.normalize(token)
        if normalized is None:
            stopwords.append(str(token))
        else:
            if normalized not in shelve:
                unknown.append(str(token))
            else:
                terms.append(normalized)
    if unknown:
        return [], stopwords, unknown
    posting_list = [shelve[term] for term in terms]
    posting_list = sorted(posting_list, key=lambda d: len(d))
    result = intersection(posting_list)
    return result, stopwords, unknown


if __name__ == '__main__':
    print("Files are creating, please wait...")

    prepro.test_corpus()

    for field in ["Director", "Starring", "Location"]:
        director_starring_location_inverted_index(shelvename=field + "_inverted_index", field=field)

    title_text_inverted_index(shelvename1="title_text_inverted_index_1", shelvename2="title_text_inverted_index_2")

    all_doc_shelve("2018_movies.json")

    print("done!")



