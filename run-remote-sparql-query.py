from pymantic import sparql

server = sparql.SPARQLServer('https://tender-hack-spb-manaslu.aa13q.ru/bigdata/sparql')

# Loading data to Blazegraph
server.update('load <file:///tmp/data.ttl>')


# Executing query
result = server.query('select * where { ?s ?p ?o }')
for b in result['results']['bindings']:
    print(b['s']['value'], b['p']['value'], b['o']['value'])