from flair.data import Sentence
from flair.nn import Classifier

from flair.splitter import SegtokSentenceSplitter

text = 'I love Berlin. This is my second sentence. JFK said "I am a Berliner" but Ronald Reagan demanded the wall be torn down.'

splitter =  SegtokSentenceSplitter()
sentences = splitter.split(text)

tagger = Classifier.load('ner-fast')
tagger.predict(sentences)


for i, sent in enumerate(sentences):
	for label in sent.get_labels('ner'):
		print(f'label : {label.value}\t entity : {label.data_point.text}')


def NER_results(text):

	splitter =  SegtokSentenceSplitter()
	sentences = splitter.split(text)
	tagger = Classifier.load('ner-fast')
	tagger.predict(sentences)

	results = []
	for i, sent in enumerate(sentences):
		for label in sent.get_labels('ner'):
			results.append((i, label.value, label.data_point.text))

	return results 