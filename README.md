## Getting started
Start rest api server:
```ssh
python rest-api.py
```
Send queries:
```ssh
curl --request POST \
  --url http://localhost:5000/search \
  --header 'content-type: application/json' \
  --data '{
	"query": "тетрадь которая имеет тврдую обложк и на кольцах еще",
	"fix-misspellings": true,
	"use-embeddings": true
}'
```