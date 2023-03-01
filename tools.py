import json
import time

from datetime import date
from newspaper import Article

def read_dictionary(FILE):
    try :
        with open(FILE) as infile:
            doc_dic = json.load(infile)
    except:
        doc_dic = False
            
    return doc_dic

def save_dictionary(dictionary,  FILE):
    with open(FILE,'w') as outfile:
        json.dump(
            dictionary, 
            outfile,
            ensure_ascii = True,
            indent = 4
            )

    return



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


'''
search_result = {
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet")
        }
'''
def save_results(search_results, query):

    DATE = str(date.today())
    t = time.localtime()
    CURRENT_TIME = time.strftime("_%H_%M_%S", t)

    for result in search_results:
        try:
            
            article = Article(result['link'])
            article.download()
            article.parse()
            
            result['text'] = article.text
        
        except:
            pass

    query_d = {
        'query' : query,
        'date' : DATE,
        'results' : search_results
    }

    save_dictionary(query_d, 'data/'+query+CURRENT_TIME+'.json')

    return