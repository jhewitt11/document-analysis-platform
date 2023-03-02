import json
import requests

from flask import Flask, render_template, jsonify, request, flash

from tools import get_summary
from tools import search_google
from tools import save_results
from tools import read_dictionary
from tools import save_dictionary


app = Flask(__name__)
app.secret_key = "chauncey_billups_lasagna_turkey"


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/summarize', methods = ['POST', 'GET'])
def summarize():

    url = str(request.form['link_input'])
    TITLE, SUMMARY = get_summary(url)
     
    flash("Title : " + TITLE)
    flash("Summary : " + SUMMARY)
    
    return render_template("index.html", fx = 'summarize')


@app.route('/search', methods = ['POST', 'GET'])
def search():

    # result from form 
    # <input class="link" type = "text" name = "link_input">
    query = str(request.form['search_input'])
    if not query :
        return "No query provided."

    search_results = search_google(query, 2)
    
    save_results(search_results, query)

    return render_template("index.html", fx = 'search')


if __name__ == '__main__':
    app.run()
    
'''
# for txt file input
    if request.method == 'POST':
        f = request.files['file']       
        url = f.read()
        url = url.decode('utf-8')
'''

#for txt file input    
#    return jsonify({'article_title': TITLE, 'article_summary' : SUMMARY})