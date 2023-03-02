import json
import requests

from flask import Flask, render_template, jsonify, request, flash

from tools import get_summary
from tools import search_google
from tools import save_google_results
from tools import flash_results
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

    query = str(request.form['search_input'])
    if not query :
        return "No query provided."


    result_dict = search_google(query, 2)
    save_google_results(result_dict, 'data/')

    flash_results(result_dict)

    return render_template("index.html", fx = 'search')


if __name__ == '__main__':
    app.run()
