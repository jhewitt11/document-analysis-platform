from flask import render_template, request, url_for, flash

import os
import re

from app import app, db
import tools


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

    #query_date_tups = tools.query_list()  
    query_date_tups = tools.select_all_queries_sql(db)     

    return render_template("NER.html", query_date_tups = query_date_tups)


'''Home page functions'''
@app.route('/search', methods = ['POST', 'GET'])
def search():

    query = str(request.form['search_input'])
    if not query :
        return "No query provided."

    query_dict = tools.search_google(query, 2)
    query_dict = tools.clean_dictionary(query_dict)
    new_qpk = tools.upload_new_data_sql(query_dict, db)
    data_bundle = tools.create_data_bundle_weaviate(new_qpk, db, export = True)


    tools.upload_data_weaviate(data_bundle)





    #tools.save_google_results(query_dict, 'data/')
    search_results = query_dict['results']
    res_l = []
    for res in search_results:
        res_l.append((res['title'], res['displayLink']))


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

    # tuple form (i, query, date)
    query_date_tups = tools.select_all_queries_sql(db)    


    return render_template('NER.html', query_date_tups = query_date_tups, fx = 'NER_list_data')


@app.route("/NER_list_documents", methods = ['POST'])
def NER_list_documents():
    '''
    Reload page and display documents from the user provided query pk.


    '''
    query_num = int(request.form['query_number_input'])

    query_date_tups = tools.select_all_queries_sql(db)  

    doc_results = tools.all_docs_from_querypk_sql(query_num, db)
  
    return  render_template('NER.html', query_date_tups = query_date_tups, query_num = query_num, doc_results = doc_results, fx = 'NER_list_documents',)


@app.route("/NER_compare_documents", methods = ['POST'])
def NER_compare_documents():
    '''
    Display NER frequency analysis from the user provided information.

    '''

    # query number
    query_num = int(request.form['query_num'])
    query_date_tups = tools.select_all_queries_sql(db)  
    
    doc_num_string = request.form['document_numbers']

    # list of indexes
    indices = [int(s) for s in re.findall(r'\d+', doc_num_string) ]

    # TESTING
    print(f'\n\nUser provided indices : {indices}\n\n')

    # get data from database
    doc_tuples = tools.docs_from_querypk_sql(query_num, indices, db)

    # analyze data and get chart.js results
    chart_data = tools.NER_build_result_dictionary(doc_tuples)


    return render_template('NER.html', query_date_tups = query_date_tups, query_num = query_num, chart_data = chart_data, fx = 'NER_compare_documents')
    

'''Q&A page functions'''
@app.route("/QA")
def QA():
    return render_template("Q&A.html")

@app.route("/chatResponse", methods = ['POST'])
def chatResponse():

    # validate user input
    # length() and tools.clean_text for now
    user_message = request.json['message']
    print('\nUser : ', user_message)

    # get oai embedding
    embedding_bundle = tools.oai_embedding(user_message)

    vector = embedding_bundle['data'][0]['embedding']

    # get context results from Weaviate query
    # openai wants related chunk(s)
    results = tools.query_weaviate(vector)

    # configure prompt for top x contexts
    # get oai chat.completion response
    #oai_response = 


    # make bundle




    bundle = tools.chat_response(user_message, results)

    return bundle