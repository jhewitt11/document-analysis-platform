from flask import Flask
from flask import render_template, jsonify, request, flash

import json
import requests
import re
import os


import tools
app = Flask(__name__)

app.secret_key = "chauncey_billups_lasagna_turkey"



'''Navigation'''
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/Summarize")
def Summarize_page():
    return render_template("Summarize.html")

@app.route("/NER")
def NER_page():

    query_date_tups = tools.query_list()   

    return render_template("NER.html", query_date_tups = query_date_tups)


'''Home page functions'''
@app.route('/search', methods = ['POST', 'GET'])
def search():

    query = str(request.form['search_input'])
    if not query :
        return "No query provided."


    result_dict = tools.search_google(query, 2)
    tools.save_google_results(result_dict, 'data/')
    
    search_results = result_dict['results']


    res_l = []
    for res in search_results:
        res_l.append((res['title'], res['displayLink']))

    print(res_l)

    return render_template("index.html", results = res_l, query = query, fx = 'search')



'''Summarize page functions '''
@app.route('/summarize_article', methods = ['POST', 'GET'])
def summarize():

    url = str(request.form['link_input'])
    TITLE, SUMMARY = tools.get_summary(url)
     
    flash("Title : " + TITLE)
    flash("Summary : " + SUMMARY)
    
    return render_template("Summarize.html", fx = 'summarize')



'''NER page functions'''
@app.route("/NER_list_data", methods = ['POST'])
def NER_list_data():

    query_date_tups = tools.query_list()

    return render_template('NER.html', query_date_tups = query_date_tups, fx = 'NER_list_data')


@app.route("/NER_list_documents", methods = ['POST'])
def NER_list_documents():

    query_num = int(request.form['query_number_input'])
    query_date_tups = tools.query_list()

    query_results = os.listdir('./data')[1:]

    dictionary_name = query_results[query_num]

    qd = tools.read_dictionary('data/'+dictionary_name)


    doc_results = []
    for i, result in enumerate(qd['results']):
        doc_results.append((i, result['title'], result['displayLink']))
  
    return  render_template('NER.html', query_date_tups = query_date_tups, query_num = query_num, doc_results = doc_results, fx = 'NER_list_documents',)


@app.route("/NER_compare_documents", methods = ['POST'])
def NER_compare_documents():

    query_num = int(request.form['query_num'])
    query_date_tups = tools.query_list()
    
    doc_num_string = request.form['document_numbers']
    doc_nums = [int(s) for s in re.findall(r'\d+', doc_num_string) ]

    chart_data = tools.NER_build_result_dictionary(query_num, doc_nums)


    return render_template('NER.html', query_date_tups = query_date_tups, query_num = query_num, chart_data = chart_data, fx = 'NER_compare_documents')
    


if __name__ == '__main__':
    app.run()