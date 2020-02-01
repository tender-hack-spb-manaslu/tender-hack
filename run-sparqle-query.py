# from pymantic import sparql

# server = sparql.SPARQLServer('http://25.29.130.188:9999/bigdata/sparql/')

# # Loading data to Blazegraph
# #server.update('load <file:///tmp/data.n3>')

# # Executing query
# result = server.query('''
# prefix ssn: <http://purl.oclc.org/NET/ssnx/ssn#> 
# prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
# prefix dul: <http://www.loa-cnr.it/ontologies/DUL.owl#> 
# prefix voice: <http://voice.iot/>  
# prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# prefix http: <http://www.w3.org/2011/http#>
# prefix cnt: <http://www.w3.org/2011/content#>
# prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>


# select DISTINCT ?query ?path ?chars ?method ?headerName ?headerValue
# {  
#   ?query a http:Request.
#   ?query http:absolutePath ?path.
#   ?query http:methodName ?method.
#   ?query http:body ?body.
#   ?body cnt:chars ?chars.
#   ?query http:headers/(rdf:first|rdf:rest)* ?header.
#   ?header http:fieldName ?headerName.
#   ?header http:fieldValue ?headerValue.
# filter (?query = <http://voice.iot/request/get_device_state>)}
# ''')
# for b in result['results']['bindings']:
#     print(f"{b['p']['value']}, {b['o']['value']}")

from pymantic import sparql

server = sparql.SPARQLServer('http://25.29.130.188:9999/blazegraph/sparql')

# Loading data to Blazegraph
#server.update('load <file:///tmp/data.n3>')

# Executing query
result = server.query('select * where { <http://blazegraph.com/blazegraph> ?p ?o }')
for b in result['results']['bindings']:
    print(b['p']['value'], b['o']['value'])
