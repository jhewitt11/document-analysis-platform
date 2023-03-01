
import json
import requests
from flask import Flask, render_template, jsonify, request, flash
from newspaper import Article

app = Flask(__name__)
app.secret_key = "chauncey_billups_lasagna_turkey"


def get_summary(url):

    try:
        article = Article(url)
    
        article.download()
        article.parse()
        article.nlp()
        
        title = article.title
        summary = article.summary
  
    except :
        title = 'Title'
        summary = 'Summary'      
    
    return title, summary

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/summarize', methods = ['POST', 'GET'])
def summarize():

    url = str(request.form['link_input'])
    TITLE, SUMMARY = get_summary(url)
     
    flash("Title : " + TITLE)
    flash("Summary : " + SUMMARY)
    
    return render_template("index.html")

@app.route('/scrape', methods = ['POST', 'GET'])
def scrape():

    # result from form 
    # <input class="link" type = "text" name = "link_input">
    query = str(request.form['search_input'])
    if not query :
        return "No query provided."


    API_KEY      = 'AIzaSyCMGE74ieu9TgQb7GGRUfmMiYyA99BFgQI'
    ENGINE_ID    = 'd7cd10591edc547dd'

    url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={ENGINE_ID}&q={query}'

    # Send built url via GET
    response = requests.get(url)
    if response.status_code != 200:
        return "Error querying Google Search."
    
    results = response.json().get('items')
    if not results:
        return "No results found."

    # Extract relevant data from the search results
    search_results = []
    for result in results:
        search_result = {
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet")
        }
        flash('Title  : ' + search_result['title'])
        flash('Link : ' + search_result['link'])

        search_results.append(search_result)
    
    return render_template("index.html")


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