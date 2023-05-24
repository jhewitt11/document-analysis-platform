import re
import json
import tools


def clean_text(text) :

    text = bytes(text, 'utf-8').decode('utf-8','ignore')
    text = re.sub('\s+', ' ', text)

    return text

def clean_dictionary(query_dict):
    '''
    Query will be excluded from cleaning in this process.

    Only fetched results will be cleaned.
    '''

    results = query_dict['results']


    for result in results:

        result['title'] = clean_text( result['title'] )
        result['link'] = clean_text( result['link'] )
        result['text'] = clean_text( result['text'] )


    return query_dict



DATA_DIR    = 'data/'
FILE        = 'US debt limit negotiation Senema_2023-05-08_13-49-48.json'

'''
with open(DATA_DIR+FILE) as file:
    qd = json.load(file)
'''


qd = tools.read_dictionary(DATA_DIR + FILE)

print(qd)

qd_clean = clean_dictionary(qd)

clean_results = qd_clean['results']


for i in range(5):
    print(f'Clean Text : {clean_results[i]["text"]}')