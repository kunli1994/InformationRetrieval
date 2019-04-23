"""
Kun Li

"""
from boolean_index import conjunctive_query
from nltk import sent_tokenize
import shelve


def dummy_search(query, shelves):
    """Return a list of movie ids that match the query, stopwords and unknown words"""
    token_list = query.split()
    ids, stopwords, unknown = conjunctive_query(token_list, shelves)
    return ids, stopwords, unknown


def dummy_movie_data(doc_id, shelvename="all_doc_shelve"):
    """Return data fields for a movie."""
    all_doc_shelve = shelve.open(shelvename, writeback=False)
    movie_object = all_doc_shelve[doc_id]
    all_doc_shelve.close()
    return movie_object


def dummy_movie_snippet(doc_id):
    """
    Return a snippet for the results page.
    Needs to include a title and a short description.
    Your snippet does not have to include any query terms, but you may want to think about implementing
    that feature. Consider the effect of normalization of index terms (e.g., stemming), which will affect
    the ease of matching query terms to words in the text.
    """
    movie_object = dummy_movie_data(doc_id, shelvename='all_doc_shelve')
    title = movie_object["Title"]
    # display the first sentence
    description = ' '.join(sent_tokenize(movie_object["Text"])[:1])
    result = (doc_id, title, description)
    return result
