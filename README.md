## About
The project aims to implement a sophisticated search algorithm using a plain `tsv` file with input entries.
## Starting REST API server
Start rest api server:
```ssh
python rest-api.py --verbose --w2v /home/dima/models/ArModel100w2v.txt --port 8080 --debug
```
Parameters:  
- `verbose` - controls quantity of active `print`s primarily during processing the query (i.e. output of tokens and lemmas)
- `w2v` - path to the `w2v` model for looking up similar words (if not set, then `w2v` model will have not been created and as a consequence server will start much faster) it is possible that in future other embeddings will be available as well (suche as bert, elmo, fasttext and so on)
- `port` - port on which web server will be running on
- `debug` - passes over directly to the `app.run` method of the `flask` module
## Sending queries
```ssh
curl --request POST \
  --url http://localhost:8080/search \
  --header 'content-type: application/json' \
  --data '{
	"query": "грачи улятели",
	"fix-misspellings": true,
	"use-embeddings": false,
	"similar-tokens-score-weight": 1.5,
	"similar-tokens-quantity": 2,
	"products-quantity": 10,
	"similar-products-quantity": 5,
	"min-word-difference-ratio": 90
}' | python -m json.tool | ascii2uni -a U -q
```
Parameters:  
- `query` - search query to use
- `fix-misspellings` - wether or not use module for fixing spelling mistakes by applying Levenstein distance
- `max-word-difference-ratio` - gives minimal score of similarity between word to fix and found fixed word for exchange to make sense
- `use-embeddings` - wether or not apply embeddings to search for similar tokens
- `similar-tokens-score-weight` - how much score brings one match of lemma or token when searching for similar words
- `similar-tokens-quantity` - how many similar tokens to consider
- `products-quantity` - how many products return as a result of direct search
- `similar-products-quantity` - how many products return as a result of search by similar words found using embeddings
Response example:  
```json
{
  "http://tender.hack.spb/1159309": {
    "name": "Кonos фильтр бумажный для кофеварок №4, 80 шт (Folie)",
    "score": 1,
    "keywords": [
      "бумажный"
    ]
  },
  "http://tender.hack.spb/1100321": {
    "name": "Полотенца бумажные 110 шт., KIMBERLY-CLARK Scott, комплект 16 шт., Slimfold, белые, 29,5х19 см, М-fold, диспенсер 601535, АРТ.5856",
    "score": 1,
    "keywords": [
      "бумажный"
    ]
  },
  "http://tender.hack.spb/1159308": {
    "name": "Кonos фильтр бумажный для кофеварок №4, 100 шт (Folie)",
    "score": 1,
    "keywords": [
      "бумажный"
    ]
  },
  "http://tender.hack.spb/1159304": {
    "name": "Кonos фильтр бумажный для кофеварки №4, 100 шт",
    "score": 1,
    "keywords": [
      "бумажный"
    ]
  },
  "http://tender.hack.spb/1161231": {
    "name": "Бумажные фильтр-мешки Karcher 5 шт. 6.904-322.0",
    "score": 1,
    "keywords": [
      "бумажный"
    ]
  }
}
```
## Additional scripts
- `make-graph.py` - to convert data from `tsv` format to `ttl`
- `good_inqury.py` - for fixing spelling mistakes
- `data_parsers.py` - for parsing `tsv` rows and converting them to `dicts`
- `calculate-name-embeddings.py` - for calculating embedding vectors of product names with `ELMo` as a base model (requires a lot of computing power)
- `load_elmo_embeddings.py` - to test that `ELMo` embeddings were saved properly
- `preprocess-user-input.py` - the main model which processes user's query - splits it into tokens, lemmatizes and connects to some other modules
- `rest-api.py` - code for starting `flask` http server
- `run-remote-sparql-query.py` - basic example of running a simple sparqle query referring to a **remote** blazegraph instance
- `run-sparql-query.py` - basic example of running a simple sparqle query referring to a **local** blazegraph instance