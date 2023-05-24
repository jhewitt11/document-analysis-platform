import json
import os

def jprint(json_in, indent_level = 2):    
    print(json.dumps(json_in, indent = indent_level))

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


def query_list():
    
    result_l = os.listdir(path='./data')[1:]

    tups = []

    for i, result in enumerate(result_l):

        split_text = result.split('_')
        tups.append((i, split_text[0], split_text[1]))

    return tups