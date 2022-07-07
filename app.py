
import json

from flask import Flask, jsonify, request
from newspaper import Article

app = Flask(__name__)



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


@app.route('/summarize', methods = ['POST'])
def summarize():
    if request.method == 'POST':
        f = request.files['file']       
        
        url = f.read()
        url = url.decode('utf-8')

        TITLE, SUMMARY = get_summary(url)
     
        return jsonify({'article_title': TITLE, 'article_summary' : SUMMARY})
    

if __name__ == '__main__':
    app.run()
    