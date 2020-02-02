from flask import Flask, request, jsonify
import json
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import argparse
from pymantic import sparql
# w2v path example: "/home/dima/models/ArModel100w2v.txt"

processor = __import__('preprocess-user-input')

W2V_EMBEDDINGS = "w2v"

app = Flask(__name__)
embeddings = {W2V_EMBEDDINGS: None}

@app.route('/search', methods=['POST'])
def foo():
    global embeddings
    global args
    data = request.json
    if 'query' not in data:
        return {"status": "error"}
    response = json.dumps(processor.search(
        query = data['query'],
        fix_misspellings = data['fix-misspellings'] if 'fix-misspellings' in data else False,
        use_embeddings = data['use-embeddings'] if 'use-embeddings' in data else False,
        w2v = embeddings[data['embeddings'] if 'embeddings' in data else W2V_EMBEDDINGS],
        similar_tokens_score_weight = data['similar-tokens-score-weight'] if 'similar-tokens-score-weight' in data else 0.5,
        similar_tokens_quantity = data['similar-tokens-quantity'] if 'similar-tokens-quantity' in data else 2,
        products_quantity = data['products-quantity'] if 'products-quantity' in data else 5,
        similar_products_quantity = data['similar-products-quantity'] if 'similar-products-quantity' in data else 5,
        verbose = args.verbose,
        min_word_difference_ratio = data['min-word-difference-ratio'] if 'min-word-difference-ratio' in data else 50,
        sparql_server = sparql.SPARQLServer(f'http://{args.sparql_host}:9999/bigdata/sparql')
    )).encode().decode("utf-8")
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--w2v', type=str, default=None)
    parser.add_argument('--sparql_host', type=str, default="localhost")
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--verbose', action="store_true")

    args = parser.parse_args()

    if args.w2v is not None:
        embeddings[W2V_EMBEDDINGS] = KeyedVectors.load_word2vec_format(datapath(args.w2v), binary=False)
    app.run(debug=args.debug, port=args.port)