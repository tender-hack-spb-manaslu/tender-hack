import argparse, csv
from rdflib import URIRef, BNode, Literal
from data_parsers import parse_data
from nltk.tokenize import RegexpTokenizer
import pymorphy2
from rdflib import Graph
from nltk.corpus import stopwords
import re


from deeppavlov import build_model
import deeppavlov
import numpy as np
from scipy import spatial
from good_inqury import fix_misspelling


import itertools
from transliterate import translit

english_token_pattern = re.compile("^[A-Za-z0-9\s-]+$")
# text = 'Samsung'
# print(english_token_pattern.match(text))
# print(translit(text, 'ru', reversed=not english_token_pattern.match(text)))
# dd
aggregate = __import__("aggregate-lemma-querying-results")


# Loading data to Blazegraph
#server.update('load <file:///tmp/data.n3>')


# Loading data to Blazegraph
#server.update('load <file:///tmp/data.ttl>')




# Executing query

def merge(dict1, dict2):
	for product in dict2:
		if product in dict1:
			dict1[product]['score'] += dict2[product]['score']
			dict1[product]['keywords'] = list(set(dict2[product]['keywords'] + dict1[product]['keywords']))
		else:
			dict1[product] = dict2[product]
	return dict1

def search(query, fix_misspellings=False, use_embeddings=False, w2v=None, similar_tokens_score_weight=0.5, similar_tokens_quantity=2, products_quantity=5, similar_products_quantity=5, verbose=False, min_word_difference_ratio=50, sparql_server=None,
	enable_good_type_diversity=False, enable_product_type_diversity=False, enable_developer_diversity=False, enable_transliteration=False):
	user_input = query

	tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
	morph = pymorphy2.MorphAnalyzer()
	russian_stopwords = stopwords.words("russian")

	tokenized_user_input = list(map(lambda word: fix_misspelling(word, min_ratio = min_word_difference_ratio, verbose = verbose) if fix_misspellings else word, [token for token in tokenizer.tokenize(user_input) if token not in russian_stopwords]))
	tokens = [token for token in tokenized_user_input] + ([translit(token, 'ru', reversed=not english_token_pattern.match(token)) for token in tokenized_user_input] if enable_transliteration else [])
	#print(tokens)
	#print(tokenized_user_input)
	lemmas = [morph.parse(token)[0].normal_form for token in tokenized_user_input] + ([morph.parse(translit(token, 'ru', reversed=not english_token_pattern.match(token)))[0].normal_form for token in tokenized_user_input] if enable_transliteration else []) #[morph.parse(token)[0].normal_form for token in tokenized_user_input]
	#elmo = build_model(deeppavlov.configs.elmo_embedder.elmo_ru_wiki, download=True)
	if verbose:
		print(f"tokens: {tokens}")
		print(f"lemmas: {lemmas}")
	products = aggregate.get_relevant_products(zip(lemmas, tokens), quantity=products_quantity, server=sparql_server, enable_developer_diversity=enable_developer_diversity, enable_product_type_diversity=enable_product_type_diversity,
		enable_good_type_diversity=enable_good_type_diversity)
	
	if use_embeddings and w2v is not None:
		similar_tokens = [token for token in list(set(itertools.chain(*[list(map(lambda pair: pair[0], w2v.most_similar(token, topn=similar_tokens_quantity))) for token in tokens]))) if morph.parse(token)[0].normal_form not in lemmas]
		similar_lemmas = [morph.parse(token)[0].normal_form for token in similar_tokens]
		if enable_transliteration:
			similar_tokens = similar_tokens + ([translit(token, 'ru', reversed=not english_token_pattern.match(token)) for token in similar_tokens] if enable_transliteration else [])
			similar_lemmas = similar_lemmas + ([translit(token, 'ru', reversed=not english_token_pattern.match(token)) for token in similar_lemmas] if enable_transliteration else [])
		if verbose:
			print(f"similar tokens: {similar_tokens}")
			print(f"similar lemmas: {similar_lemmas}")
		similar_products = aggregate.get_relevant_products(zip(similar_lemmas, similar_tokens), quantity=similar_products_quantity, weight=similar_tokens_score_weight, server=sparql_server, enable_developer_diversity=enable_developer_diversity, enable_product_type_diversity=enable_product_type_diversity,
		enable_good_type_diversity=enable_good_type_diversity)
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
