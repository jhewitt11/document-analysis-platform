import json
import requests

from flask import Flask, render_template, jsonify, request, flash

import tools



app = Flask(__name__)
app.secret_key = "chauncey_billups_lasagna_turkey"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/NER")
def NER():
    return render_template("NER.html")


@app.route('/summarize', methods = ['POST', 'GET'])
def summarize():

    url = str(request.form['link_input'])
    TITLE, SUMMARY = tools.get_summary(url)
     
    flash("Title : " + TITLE)
    flash("Summary : " + SUMMARY)
    
    return render_template("index.html", fx = 'summarize')


@app.route('/search', methods = ['POST', 'GET'])
def search():

    query = str(request.form['search_input'])
    if not query :
        return "No query provided."


    result_dict = tools.search_google(query, 2)
    tools.save_google_results(result_dict, 'data/')

    tools.flash_results(result_dict)

    return render_template("index.html", fx = 'search')


if __name__ == '__main__':
    app.run()
