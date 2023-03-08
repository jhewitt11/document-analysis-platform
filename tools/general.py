import json
import os

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
    return os.listdir(path = './data')