                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
from flair.data import Sentence
from flair.nn import Classifier
from flair.splitter import SegtokSentenceSplitter

from .general import read_dictionary
from .general import query_list

import requests


'''
def NER_results_HF(text):
'''
#NER via HF API
'''
settings_dict = read_dictionary('settings.json')

HF_KEY = settings_dict["HF_KEY"]


## huggingface api call

return results
'''

def NER_results(text):
	'''
	Create results list of Named Entities from a text document using Flair framework.

	Flair annotates sentences and get_labels() is used to access the data. 

	label.value : Tagged label
	label.data_point.text : Text associated with label

	Flair citation : 
	@inproceedings{akbik2019flair,
	  title={{FLAIR}: An easy-to-use framework for state-of-the-art {NLP}},
	  author={Akbik, Alan and Bergmann, Tanja and Blythe, Duncan and Rasul, Kashif and Schweter, Stefan and Vollgraf, Roland},
	  booktitle={{NAACL} 2019, 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics (Demonstrations)},
	  pages={54--59},
	  year={2019}
	}

	Input :
	text : text document

	Output :
	results : List of result tuples. (sentence index, label, text)
	'''

	splitter =  SegtokSentenceSplitter()
	sentences = splitter.split(text)
	tagger = Classifier.load('ner-fast')
	tagger.predict(sentences)

	results = []
	for i, sent in enumerate(sentences):
		for label in sent.get_labels('ner'):
			results.append((i, label.value, label.data_point.text))
			#print(results[-1])

	return results 




def NER_build_result_dictionary(document_tuples):
	'''
	Build results from NER task for chart.js visualization.

	Input :
	document_tuples : Tuples of information for each document being analyzed.

	Output :
	chart_data : NER data from each document compiled in a result for chart.js display.
	'''

	titles, display_links, texts = document_tuples

	ENTITY_ID = {}
	ENTITY_COUNT_LIST = []

	for i, text in enumerate(texts) :

		entities_found = {}

		results = NER_results(text)
		for result in results:

			if result[1] == 'PER':
				entity = result[2]

				if ENTITY_ID.get(entity) == None:
					ENTITY_ID[entity] = len(ENTITY_ID)

				if entities_found.get(ENTITY_ID[entity]):
					entities_found[ENTITY_ID[entity]] += 1
				else:
					entities_found[ENTITY_ID[entity]] = 1

		ENTITY_COUNT_LIST.append(entities_found)


	chart_dataset = []

	for i, ECL in enumerate(ENTITY_COUNT_LIST):
		data_dict = {}

		data_dict['label'] = display_links[i]

		data = []

		for i in range(len(ENTITY_ID)):
			if ECL.get(i) == None :
				data.append(0)
			else:
				data.append(ECL.get(i))

		data_dict['data'] = data
		chart_dataset.append(data_dict)

	chart_data = {
		'labels' : list(ENTITY_ID.keys()),
		'datasets' : chart_dataset
	}

	return chart_data

