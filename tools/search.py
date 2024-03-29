import json
import requests
import time

from flask import flash

from datetime import date
from newspaper import Article

from .general import read_dictionary
from .general import save_dictionary

from .clean import clean_text



def save_google_results(result_dict, directory = ''):
    '''
    Save results dictionary from search_google() in a consistent format.

    Input :
    result_dict : dictionary of search results
    directory : directory to save json file

    Output :
    None
    '''

    query = result_dict['query']
    date = result_dict['date']
    time = result_dict['time']

    location = directory + query +'_'+date+'_'+time + '.json'

    save_dictionary(result_dict, location)

    return


def search_google(query, number_pages):
    '''
    Build dictionary from results of google query.

    Input :
    query : search input string
    number_pages : number of pages for Google to return

    Output :
    Results dictionary of format..
        query_d = {
            'query' : query,
            'date' : DATE,
            'time' : CURRENT_TIME,
            'totalResults' : totalResults, 
            'searchTime' : searchTime,
            'results' : search_results,
            'failedExtractions' : failed_extractions
        }
    '''
    DATE = str(date.today())
    t = time.localtime()
    CURRENT_TIME = time.strftime("%H-%M-%S", t)

    settings_dict = read_dictionary('settings.json')
    API_KEY     = settings_dict['GOOGLE_KEY']
    ENGINE_ID   = settings_dict['ENGINE_ID']

    search_results = []
    failed_extractions = []
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
                print(f'Failed to retrieve article #{num} error')

            if article.text != '':
                search_result = {
                    "title":        result.get("title"),
                    "link":         result.get("link"),
                    "displayLink" : result.get("displayLink"),
                    "snippet":      result.get("snippet"),
                    #"pagemap":      result.get("pagemap"),
                    "index":        start_index + num,
                    "text":         article.text
                }
                search_results.append(search_result)

            else:
                failed_result  = {
                    "title":        result.get("title"),
                    "link":         result.get("link"),
                    "displayLink" : result.get("displayLink"),
                    "index":        start_index + num,
                }
                failed_extractions.append(failed_result)

        totalResults = response.json().get('searchInformation').get('totalResults')
        searchTime = response.json().get('searchInformation').get('searchTime')

        query_d = {
            'query' : query,
            'date' : DATE,
            'time' : CURRENT_TIME,
            'totalResults' : totalResults,
            'searchTime' : searchTime,
            'results' : search_results,
            'failedResults' : failed_extractions
        }

    return query_d


def flash_results(result_dict):
    '''
    Flash information to be rentered in HTML. Messages sent by flash() are
    accessed by get_flashed_messages() in HTML.

    Input : 
    result_dict : dictionary of search results

    Output :
    None
    '''

    search_results = result_dict['results']

    for rd in search_results :
        flash("Title : " + rd['title'], 'title')
        flash("Source : " + rd['displayLink'], 'link')

    return




