import json
import requests
import re

from flask import Flask, render_template, jsonify, request, flash

import tools


app = Flask(__name__)
app.secret_key = "chauncey_billups_lasagna_turkey"

'''Navigation'''
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Summarize")
def Summarize_page():
    return render_template("Summarize.html")


@app.route("/NER")
def NER_page():
    return render_template("NER.html")


'''Home page functions'''
@app.route('/search', methods = ['POST', 'GET'])
def search():

    query = str(request.form['search_input'])
    if not query :
        return "No query provided."


    result_dict = tools.search_google(query, 2)
    tools.save_google_results(result_dict, 'data/')

    tools.flash_results(result_dict)

    return render_template("index.html", fx = 'search')



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
  
    return  render_template('NER.html', fx = 'NER_list_documents', query_num = query_num)


@app.route("/NER_compare_documents", methods = ['POST'])
def NER_compare_documents():

    query_num = int(request.form['query_num'])
    
    doc_num_string = request.form['document_numbers']
    doc_nums = [int(s) for s in re.findall(r'\d+', doc_num_string) ]

    chart_data = tools.NER_build_result_dictionary(query_num, doc_nums)


    return render_template('NER.html', query_num = query_num, chart_data = chart_data, fx = 'NER_compare_documents')
    

if __name__ == '__main__':
    app.run()
