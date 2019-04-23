"""
Kun Li

Start the web page and connected frond end.
"""

from flask import Flask, render_template, request
from boolean_search import dummy_search, dummy_movie_data, dummy_movie_snippet
from boolean_index import intersection
import shelve

# Create an instance of the flask application within the appropriate namespace (__name__).
# By default, the application will be listening for requests on port 5000.
app = Flask(__name__)


# Welcome page
# Python decorators are used by flask to associate url routes to functions.
@app.route("/")
def query():
    """For top level route ("/"), simply present a query page."""
    return render_template('query_page.html')


# This takes queries and turns them into results
@app.route("/results/<int:page_num>", methods=['POST'])
def results(page_num):
    """Generate a result set for a query and present the 10 results starting with <page_num>."""
    titile_text_shelve_1 = shelve.open("titile_text_inverted_index_1", writeback=False)
    titile_text_shelve_2 = shelve.open("title_text_inverted_index_2", writeback=False)
    director_shelve = shelve.open("Director_inverted_index", writeback=False)
    starring_shelve = shelve.open("Starring_inverted_index", writeback=False)
    location_shelve = shelve.open("Location_inverted_index", writeback=False)
    category = ['query', 'director', 'starring', 'location']
    shelve_dict = {'query': titile_text_shelve_1, 'director': director_shelve,
                   'location': location_shelve, 'starring': starring_shelve}
    # shelves for queries over terms in different category
    unknown_terms = []
    skipped_words = []
    lis_ID = []
    queries = []
    for field in category:
        raw_query = request.form[field]
        queries.append(raw_query)
        if raw_query:
            ids, skippedwords, unk = dummy_search(raw_query, shelve_dict[field])
            lis_ID.append(ids)
            skipped_words.extend(skippedwords)
            unknown_terms.extend(unk)
    lis_ID[0].extend(dummy_search(request.form['query'], titile_text_shelve_2)[0])
    movie_ids = intersection(lis_ID)
    num_hits = len(movie_ids)  # Save the number of hits to display later
    movie_ids = movie_ids[((page_num - 1) * 10):(page_num * 10)]  # Limit of 10 results per page
    movie_results = list(map(dummy_movie_snippet, movie_ids))  # Get movie snippets: title, abstract, etc.
    return render_template('results_page.html', orig_query1=queries[0],orig_query2=queries[1],
                           orig_query3=queries[2], orig_query4=queries[3],results=movie_results,
                           srpn=page_num, len=len(movie_ids), unknown_terms=unknown_terms,
                           skipped_words=skipped_words, total_hits=num_hits)


# Process requests for movie_data pages
@app.route('/movie_data/<film_id>')
def movie_data(film_id):
    """Given the doc_id for a film, present the title and text (optionally structured fields as well)
    for the movie."""
    data = dummy_movie_data(film_id, shelvename='all_doc_shelve')  # Get all of the info for a single movie
    return render_template('doc_data_page.html', data=data)


# If this module is called in the main namespace, invoke app.run()
if __name__ == "__main__":
    app.run()
