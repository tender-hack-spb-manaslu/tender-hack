#from pymantic import sparql

#server = sparql.SPARQLServer('http://25.29.130.188:9999/bigdata/sparql')

# Loading data to Blazegraph
#server.update('load <file:///tmp/data.ttl>')


# Executing query
def get_products(lemma, label, server=None):
    # result = server.query(f"""
    # prefix tender: <http://tender.hack.spb/> 
    # Select DISTINCT ?uri ?nameLabel where {{?uri tender:token ?token. ?uri tender:hasName ?name. ?name tender:label ?nameLabel. ?token tender:label ?tokenLabel. ?token tender:lemma ?lemma.  {{?token tender:lemma "{lemma}"}} UNION {{?token tender:label "{label}"}}}}
    # """)
    result = server.query(f"""
    prefix tender: <http://tender.hack.spb/>
    Select DISTINCT ?uri ?nameLabel ?goodTypeLabel ?productTypeLabel ?developerLabel where {{?uri tender:token ?token. ?uri tender:hasName ?name. ?name tender:label ?nameLabel. ?token tender:label ?tokenLabel. ?token tender:lemma ?lemma. 
    ?uri tender:hasGoodType ?goodType . ?goodType tender:label ?goodTypeLabel.
    ?uri tender:hasProductType ?productType . ?productType tender:label ?productTypeLabel.
    OPTIONAL {{?uri tender:hasDeveloper ?developer . ?developer tender:label ?developerLabel.}}
    {{?token tender:lemma "{lemma}"}} UNION {{?token tender:label "{label}"}}}}
    """)
    return [item['uri']['value'] for item in result['results']['bindings']],\
           {item['uri']['value']: item['nameLabel']['value'] for item in result['results']['bindings']},\
           {item['uri']['value']: item['goodTypeLabel']['value'] for item in result['results']['bindings']},\
           {item['uri']['value']: item['productTypeLabel']['value'] for item in result['results']['bindings']},\
           {item['uri']['value']: item['developerLabel']['value'] for item in result['results']['bindings']}
# scores = {}
# for b in result['results']['bindings']:
def get_relevant_products(tokens, quantity=5, weight=1, server=None, enable_good_type_diversity=False, enable_product_type_diversity=False, enable_developer_diversity=False):
    scores = {}
    names = {}
    keywords = {}
    good_types = {}
    product_types = {}
    developers = {}
    for lemma, label in tokens:
        uris, names_, good_types_, product_types_, developers_ = get_products(lemma, label, server = server)
        for uri in uris:
            if uri in scores:
                scores[uri] += 1
                keywords[uri].append(lemma)
            else:
                scores[uri] = 1
                names[uri] = names_[uri]
                keywords[uri] = [lemma]
                good_types[uri] = good_types_[uri]
                product_types[uri] = product_types_[uri]
                developers[uri] = developers_[uri]
    
    lookup_result = []
    quantity_counter = 0
    diversity_relevant_labels_history = []
    # Work for diversity
    for item in sorted([(key, scores[key]) for key in scores], key = lambda item: -item[1]):
        if quantity_counter >= quantity:
            break
        lookup_entry = {"id": item[0], "name": names[item[0]], "score": item[1]*weight, "keywords": keywords[item[0]], "product-type": product_types[item[0]], "good-type": good_types[item[0]], "developer": developers[item[0]]}
        current_diversity_relevant_labels = {}
        #print(lookup_entry)
        if enable_developer_diversity:
            current_diversity_relevant_labels['developer'] = lookup_entry['developer']
        if enable_good_type_diversity:
            current_diversity_relevant_labels['good-type'] = lookup_entry['good-type']
        if enable_product_type_diversity:
            current_diversity_relevant_labels['product-type'] = lookup_entry['product-type']
        if len(list(current_diversity_relevant_labels.keys())) == 0 or current_diversity_relevant_labels not in diversity_relevant_labels_history:
            #print(diversity_relevant_labels_history, current_diversity_relevant_labels)
            lookup_result.append(lookup_entry)
            diversity_relevant_labels_history.append(current_diversity_relevant_labels)
            quantity_counter += 1

    # If got too few samples, then disable high-diversity mode
    if quantity_counter < quantity:
        for item in sorted([(key, scores[key]) for key in scores], key = lambda item: -item[1]):
            if quantity_counter >= quantity:
                break
            if item not in lookup_result:
                lookup_entry = {"id": item[0], "name": names[item[0]], "score": item[1]*weight, "keywords": keywords[item[0]], "product-type": product_types[item[0]], "good-type": good_types[item[0]], "developer": developers[item[0]]}
                lookup_result.append(lookup_entry)
                quantity_counter += 1

    return {entry['id']: {key: entry[key] for key in entry if key != 'id'} for entry in lookup_result}

    # results = {item[0]: {"name": names[item[0]], "score": item[1]*weight, "keywords": keywords[item[0]], "product-type": product_types[item[0]], "good-type": good_types[item[0]], "developer": developers[item[0]]}
    # for item in sorted([(key, scores[key]) for key in scores], key = lambda item: -item[1])[:quantity]}
    # return results

if __name__ == "__main__":
    print(get_relevant_products([("цветной", "цветные"), ("фломастер", "фломастеры")]))
