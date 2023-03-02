import json
import requests
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


def save_google_results(result_dict, directory = ''):

    query = result_dict['query']
    date = result_dict['date']
    time = result_dict['time']

    location = directory + query +'_'+date+'_'+time + '.json'

    save_dictionary(result_dict, location)

    return


def search_google(query, number_pages):

    DATE = str(date.today())
    t = time.localtime()
    CURRENT_TIME = time.strftime("%H-%M-%S", t)

    settings_dict = read_dictionary('settings.json')
    API_KEY     = settings_dict['API_KEY']
    ENGINE_ID   = settings_dict['ENGINE_ID']

    search_results = []
    for k in range(number_pages):

        start_index = 1 + (k*10)

        url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={ENGINE_ID}&q={query}&start={start_index}'
        response = requests.get(url)

        # Manage errors        
        if response.status_code != 200:
            return "Error querying Google Search."

        results = response.json().get('items')
        if not results:
            return "No results found."

        # Extract relevant data from the search results
        for num, result in enumerate(results):
            try:
                article = Article(result['link'])
                article.download()
                article.parse()

            except:
                print('error')

            search_result = {
                "title":        result.get("title"),
                "link":         result.get("link"),
                "displayLink" : result.get("displayLink"),
                "text":         article.text,
                "snippet":      result.get("snippet"),
                #"pagemap":      result.get("pagemap"),
                "index":        start_index + num,
            }

            search_results.append(search_result)

        totalResults = response.json().get('searchInformation').get('totalResults')
        searchTime = response.json().get('searchInformation').get('searchTime')

        query_d = {
            'query' : query,
            'date' : DATE,
            'time' : CURRENT_TIME,
            'totalResults' : totalResults,
            'searchTime' : searchTime,
            'results' : search_results
        }

    return query_d