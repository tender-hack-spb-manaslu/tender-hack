from pymantic import sparql

server = sparql.SPARQLServer('http://25.29.130.188:9999/bigdata/sparql')

# Loading data to Blazegraph
#server.update('load <file:///tmp/data.ttl>')


# Executing query
def get_products(lemma, label):
	result = server.query(f"""
	prefix tender: <http://tender.hack.spb/> 
	Select DISTINCT ?uri ?nameLabel where {{?uri tender:token ?token. ?uri tender:hasName ?name. ?name tender:label ?nameLabel. ?token tender:label ?tokenLabel. ?token tender:lemma ?lemma.  {{?token tender:lemma "{lemma}"}} UNION {{?token tender:label "{label}"}}}}
	""")
	return [item['uri']['value'] for item in result['results']['bindings']], {item['uri']['value']: item['nameLabel']['value'] for item in result['results']['bindings']}
# scores = {}
# for b in result['results']['bindings']:
def get_relevant_products(tokens, quantity=5, weight=1):
	scores = {}
	names = {}
	for lemma, label in tokens:
		uris, names_ = get_products(lemma, label)
		for uri in uris:
			if uri in scores:
				scores[uri] += 1
				#print(names[uri])
			else:
				scores[uri] = 1
				names[uri] = names_[uri]
	results = {item[0]: {"name": names[item[0]], "score": item[1]*weight} for item in sorted([(key, scores[key]) for key in scores], key = lambda item: -item[1])[:quantity]}
	return results

if __name__ == "__main__":
	print(get_relevant_products([("цветной", "цветные"), ("фломастер", "фломастеры")]))
