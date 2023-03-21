from flair.data import Sentence
from flair.nn import Classifier
from flair.splitter import SegtokSentenceSplitter

from .general import read_dictionary
from .general import query_list

text = 'I love Berlin. This is my second sentence. JFK said "I am a Berliner" but Ronald Reagan demanded the wall be torn down.'

splitter =  SegtokSentenceSplitter()
sentences = splitter.split(text)

tagger = Classifier.load('ner-fast')
tagger.predict(sentences)



def NER_results(text):

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




def NER_build_result_dictionary(query_num, doc_nums):
	'''
	Build results for chart.js visualization.
	'''

	query_result_name = query_list()[1:][query_num]
	query_result = read_dictionary('./data/'+query_result_name)

	search_results = query_result['results']

	doc_items = [search_results[k] for k in doc_nums]

	titles = [item['title'] for item in doc_items]
	display_links = [item['displayLink'] for item in doc_items]
	texts = [item['text'] for item in doc_items]



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


	print(ENTITY_ID)
	print(ENTITY_COUNT_LIST)

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

	print(chart_data)

	return chart_data

