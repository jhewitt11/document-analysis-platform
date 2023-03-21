import json
import requests

from flask import Flask, render_template, jsonify, request, flash

import tools



app = Flask(__name__)
app.secret_key = "chauncey_billups_lasagna_turkey"

'''
Navigation
'''
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/NER_page")
def NER_page():
    return render_template("NER.html")


'''
Home page functions
'''
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


'''
NER page functions
'''
@app.route("/NER_list_data", methods = ['POST'])
def NER_list_data():

    query_results = tools.query_list()[1:]

    for i, result in enumerate(query_results):
        flash('#'+str(i)+'   '+result)

    return render_template('NER.html', fx = 'NER_list_data')

@app.route("/NER_list_documents", methods = ['POST'])
def NER_list_documents():
    
    query_num = int(request.form['query_number_input'])
    query_results = tools.query_list()[1:]
    dictionary_name = query_results[query_num]

    qd = tools.read_dictionary('data/'+dictionary_name)
    for i, result in enumerate(qd['results']):
        flash('#'+str(i)+'___'+result['title'] +'___' +result['displayLink'])
  
    return  render_template('NER.html', fx = 'NER_list_documents')

@app.route("/NER_compare_documents", methods = ['POST'])
def NER_compare_documents():

    return
    



if __name__ == '__main__':
    app.run()
