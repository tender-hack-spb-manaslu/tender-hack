import argparse, csv
from rdflib import URIRef, BNode, Literal
from data_parsers import parse_data
from nltk.tokenize import RegexpTokenizer
import pymorphy2
from rdflib import Graph
from nltk.corpus import stopwords
import re

from pymantic import sparql
from deeppavlov import build_model
import deeppavlov
import numpy as np
from scipy import spatial
from good_inqury import fix_misspelling


import itertools

aggregate = __import__("aggregate-lemma-querying-results")


# Loading data to Blazegraph
#server.update('load <file:///tmp/data.n3>')

server = sparql.SPARQLServer('https://tender-hack-spb-manaslu.aa13q.ru/bigdata/sparql')

# Loading data to Blazegraph
#server.update('load <file:///tmp/data.ttl>')




# Executing query

def merge(dict1, dict2):
	for product in dict2:
		if product in dict1:
			dict1[product]['score'] += dict2[product]['score']
		else:
			dict1[product] = dict2[product]
	return dict1

def search(query, fix_misspellings=False, use_embeddings=False, w2v=None):
	user_input = query

	tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
	morph = pymorphy2.MorphAnalyzer()
	russian_stopwords = stopwords.words("russian")

	tokenized_user_input = list(map(fix_misspelling if fix_misspellings else lambda i: i, [token for token in tokenizer.tokenize(user_input) if token not in russian_stopwords]))
	tokens = [token for token in tokenized_user_input]
	#print(tokens)
	lemmas = [morph.parse(token)[0].normal_form for token in tokenized_user_input]
	#elmo = build_model(deeppavlov.configs.elmo_embedder.elmo_ru_wiki, download=True)
	products = aggregate.get_relevant_products(zip(lemmas, tokens))
	
	if use_embeddings and w2v is not None:
		similar_tokens = [token for token in list(set(itertools.chain(*[list(map(lambda pair: pair[0], w2v.most_similar(token, topn=2))) for token in tokens]))) if morph.parse(token)[0].normal_form not in lemmas]
		similar_lemmas = [morph.parse(token)[0].normal_form for token in similar_tokens]
		print(similar_tokens, similar_lemmas)
		similar_products = aggregate.get_relevant_products(zip(similar_lemmas, similar_tokens), weight=0.5)
		return merge(products, similar_products)
	else:
		return products


if __name__ == "__main__":

	
	#print(dir(w2v_model))
	#print(w2v_model.most_similar('тетрадь', topn=10))

	parser = argparse.ArgumentParser()

	parser.add_argument('--query', type=str, default='хочу купть дешёвую тетрадь в плотной картонной обложке')
	parser.add_argument('--fix_misspellings', action="store_true")
	parser.add_argument('--embeddings', action="store_true")

	args = parser.parse_args()

	search(args.query, args.fix_misspellings, args.embeddings)

	# print(elmo([tokens])[0])

	# tokens_embedding = np.mean(elmo([tokens])[0], axis=0)
	# lemmas_embedding = np.mean(elmo([lemmas])[0], axis=0)

	# print(f"elmo embeddings (tokens): {tokens_embedding}")
	# print(f"elmo embeddings (lemmas): {lemmas_embedding}")

	# distance = 1 - spatial.distance.cosine(tokens_embedding, lemmas_embedding)
	# print(distance)
	# # Executing query
	# for lemma in lemmas:
	# 	result = server.query(f'prefix tender: <http://tender.hack.spb/> Select ?uri ?token ?lemma ?nameLabel where {{?name tender:label ?nameLabel. ?uri tender:hasName ?name. ?uri tender:token ?token. ?token tender:label ?tokenLabel; tender:lemma ?lemma. FILTER (?token="{lemma}" || ?lemma="{lemma}")}}')
	# 	for b in result['results']['bindings']:
	# 		print(b['nameLabel']['value'])