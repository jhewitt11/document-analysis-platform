import json
import os

def jprint(json_in, indent_level = 2):
    '''
    Prints json files with indentations.

    Input :
    json_in : json file to be printed
    indent_level : size of indent when printing

    Output:
    None
    '''    
    print(json.dumps(json_in, indent = indent_level))

    return None

def read_dictionary(FILE):
    '''
    Reads .json file and returns dictionary

    Input :
    FILE : file to be read

    Output :
    doc_dic : dictionary
    '''
    try :
        with open(FILE) as infile:
            doc_dic = json.load(infile)
    except:
        doc_dic = False

    return doc_dic


def save_dictionary(dictionary,  FILE):
    '''
    Save dictionary provided as a json in file directory.

    Input:
    dictionary : dictionary
    FILE : file directory location for output

    Output:
    None
    '''
    with open(FILE,'w') as outfile:
        json.dump(
            dictionary, 
            outfile,
            ensure_ascii = True,
            indent = 4
            )
    return


def query_list():
    '''
    Return list of contents in data directory. Files names are split and results returned as tuples.

    File name convention can be found in save_google_results()

    Input :
    None

    Output :
    tups : List of tuples 
    '''
    result_l = os.listdir(path='./data')[1:]

    tups = []

    for i, result in enumerate(result_l):

        split_text = result.split('_')
        tups.append((i, split_text[0], split_text[1]))

    return tups