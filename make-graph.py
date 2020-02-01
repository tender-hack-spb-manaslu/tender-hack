import argparse, csv
from rdflib import URIRef, BNode, Literal
from data_parsers import parse_data
from nltk.tokenize import RegexpTokenizer
import pymorphy2
from rdflib import Graph
from nltk.corpus import stopwords
import re

g = Graph()


# g.add( (bob, RDF.type, FOAF.Person) )
# g.add( (bob, FOAF.name, name) )
# g.add( (bob, FOAF.knows, linda) )
# g.add( (linda, RDF.type, FOAF.Person) )
# g.add( (linda, FOAF.name, Literal('Linda') ) )

# print g.serialize(format='turtle')

# bob = URIRef("http://example.org/people/Bob")
# linda = BNode() # a GUID is generated

# name = Literal('Bob') # passing a string
# age = Literal(24) # passing a python int
# height = Literal(76.5) # passing a python float

name_to_ids = {}
ids = {}

def get_id(name, category):
	global ids
	if category in name_to_ids:
		if name in name_to_ids[category]:
			return name_to_ids[category][name], False
	else:
		name_to_ids[category] = {}
	if category in ids:
		ids[category] += 1
	else:
		ids[category] = 0
	name_to_ids[category][name] = ids[category]
	return ids[category], True

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('--input_file', type=str, default='data.tsv')
	parser.add_argument('--output_file', type=str, default='data.ttl')

	args = parser.parse_args()

	tokenizer = RegexpTokenizer('[\wёЁ]+|\$[\d\.]+|\S+')
	num_tokenizer = RegexpTokenizer('[0-9\.]+|\w+')
	morph = pymorphy2.MorphAnalyzer()
	skip_token_pattern = re.compile(".*(?:(\.|:|,|\"|-)+).*") #re.compile(".*(?:(?:[0-9]+)|(?:(\.|:|,|\"|-)+)).*")

	russian_stopwords = stopwords.words("russian")
	for data_chunk in parse_data(args.input_file):
		product = URIRef(f"http://tender.hack.spb/{data_chunk['id']}")
		label = URIRef(f"http://tender.hack.spb/label")
		lemma = URIRef(f"http://tender.hack.spb/lemma")
		token_ref = URIRef(f"http://tender.hack.spb/token")

		# Add names
		product_name = URIRef(f"http://tender.hack.spb/{data_chunk['id']}/name")
		has_name = URIRef(f"http://tender.hack.spb/hasName")
		name = Literal(data_chunk['name'])

		g.add((product, has_name, product_name))
		g.add((product_name, label, name))

		# Add tokens
		for token in tokenizer.tokenize(data_chunk['name']):
			if token not in russian_stopwords and not skip_token_pattern.match(token):
				intermediate_token_node = BNode()
				token_label = Literal(token.lower())
				token_lemma = Literal(morph.parse(token_label)[0].normal_form)
				g.add((intermediate_token_node, label, token_label))
				g.add((intermediate_token_node, lemma, token_lemma))
				g.add((product, token_ref, intermediate_token_node))

		# Add developer
		product_developer = URIRef(f"http://tender.hack.spb/{get_id(data_chunk['developer'], 'developer')[0]}/developer")
		has_developer = URIRef(f"http://tender.hack.spb/hasDeveloper")
		developer_name = Literal(data_chunk['developer'])

		g.add((product, has_developer, product_developer))
		g.add((product_developer, label, developer_name))

		# Add product type
		id, added = get_id(data_chunk['product-type'], 'product-type')
		product_type = URIRef(f"http://tender.hack.spb/{id}/product-type")
		has_product_type = URIRef(f"http://tender.hack.spb/hasProductType")
		product_type_name = Literal(data_chunk['product-type'])

		g.add((product, has_product_type, product_type))
		g.add((product_type, label, product_type_name))

		if added:
			for token in tokenizer.tokenize(product_type_name):
				if token not in russian_stopwords and not skip_token_pattern.match(token):
					intermediate_token_node = BNode()
					token_label = Literal(token.lower())
					token_lemma = Literal(morph.parse(token_label)[0].normal_form)
					g.add((intermediate_token_node, label, token_label))
					g.add((intermediate_token_node, lemma, token_lemma))
					g.add((product_type, token_ref, intermediate_token_node))

		# Add good type
		id, added = get_id(data_chunk['good-type'], 'good-type')
		good_type = URIRef(f"http://tender.hack.spb/{id}/good-type")
		has_good_type = URIRef(f"http://tender.hack.spb/hasGoodType")
		good_type_name = Literal(data_chunk['good-type'])

		g.add((product, has_good_type, good_type))
		g.add((good_type, label, good_type_name))

		if added:
			for token in tokenizer.tokenize(good_type_name):
				if token not in russian_stopwords and not skip_token_pattern.match(token):
					intermediate_token_node = BNode()
					token_label = Literal(token.lower())
					token_lemma = Literal(morph.parse(token_label)[0].normal_form)
					g.add((intermediate_token_node, label, token_label))
					g.add((intermediate_token_node, lemma, token_lemma))
					g.add((good_type, token_ref, intermediate_token_node))

		# Add numeric fields
		# quantity = URIRef(f"http://tender.hack.spb/quantity")
		# for field_name in ["length", "width", "height", "diameter", "warranty", "weight", "volume"]:
		# 	has_feature = URIRef(f"http://tender.hack.spb/has{field_name.capitalize()}")
		# 	field_value = data_chunk[field_name]
		# 	if field_value != "NULL":
		# 		tokenized_field_value = num_tokenizer.tokenize(field_value)
		# 		intermediate_feature_node = BNode()
		# 		if len(tokenized_field_value) == 2:
		# 			try:
		# 				g.add((product, has_feature, intermediate_feature_node))
		# 				g.add((intermediate_feature_node, quantity, Literal(float(tokenized_field_value[0]))))
		# 				g.add((intermediate_feature_node, label, Literal(tokenized_field_value[1])))
		# 				continue
		# 			except ValueError:
		# 				pass
		# 		g.add((intermediate_feature_node, label, Literal(field_value)))

		

		# Add product-type
		# product_developer = URIRef(f"http://tender.hack.spb/{id}/developer")
		# has_developer = URIRef(f"http://tender.hack.spb/hasDeveloper")
		# developer_name = Literal(data_chunk['developer'])

		# g.add((product, has_developer, product_developer))
		# g.add((product_developer, label, name))


		# product_tokens = URIRef(f"http://tender.hack.spb/{data_chunk['id']}/tokens")
		# tokens = URIRef(f"http://tender.hack.spb/tokens")
		# has_tokens = URIRef(f"http://tender.hack.spb/hasTokens")
		# name = Literal(data_chunk['name'])

		# g.add((product, has_tokens, product_tokens))
		# g.add((product_tokens, label, name))



		#print(data_chunk)
print(g.serialize(format='turtle').decode('utf-8'))	