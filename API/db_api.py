
import requests



def get_queries():

    base_url  = 'http://localhost:5000'
    endpoint = '/queries'

    url = base_url + endpoint

    response = requests.get(url)

    if response.status_code == 200 :
        return response.json() 

    else:
        print('Error : ', response.status_code)
        return None



def get_documents(query_id):

    return

