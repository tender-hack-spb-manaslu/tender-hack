from pymantic import sparql
from rdflib import Graph
from nltk.tokenize import RegexpTokenizer
import pymorphy2
from nltk.corpus import stopwords
from deeppavlov import build_model
import deeppavlov
import numpy as np
from pickle import dump
import sys
#server = sparql.SPARQLServer('https://tender-hack-spb-manaslu.aa13q.ru/bigdata/sparql')

if __name__ == "__main__":
	g = Graph()
	g.parse(sys.argv[-1], format="ttl")
	elmo = build_model(deeppavlov.configs.elmo_embedder.elmo_ru_wiki, download=True)

	result = g.query(f'prefix tender: <http://tender.hack.spb/> select ?uri ?nameLabel where {{?name tender:label ?nameLabel. ?uri tender:hasName ?name.}}')
	
	lemma_embeddings = {}
	token_embeddings = {}
	i = 0

	for b in result:
		i += 1
		print(i)
		tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
		morph = pymorphy2.MorphAnalyzer()
		russian_stopwords = stopwords.words("russian")

		tokenized_name = tokenizer.tokenize(b[1])
		tokens = [token for token in tokenized_name if token not in russian_stopwords]
		lemmas = [morph.parse(token)[0].normal_form for token in tokenized_name if token not in russian_stopwords]
		
		#print(tokens, lemmas)

		tokens_embedding = np.mean(elmo([tokens])[0], axis=0)
		lemmas_embedding = np.mean(elmo([lemmas])[0], axis=0)

		lemma_embeddings[str(b[0])] = tokens_embedding
		token_embeddings[str(b[0])] = lemmas_embedding

		#print(b[0], b[1])
		# print('ll')
		# print(b['nameLabel']['value'])
	

	with open("lemmas_embeddings.pkl", "wb") as f:
		dump(lemma_embeddings, f)
	with open("tokens_embeddings.pkl", "wb") as f:
		dump(token_embeddings, f)
