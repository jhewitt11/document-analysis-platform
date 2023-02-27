
import json

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