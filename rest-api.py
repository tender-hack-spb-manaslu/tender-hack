from flask import Flask, request, jsonify
import json
from gensim.models import KeyedVectors
from gensim.test.utils import datapath

processor = __import__('preprocess-user-input')

app = Flask(__name__)
w2v_model = None

@app.route('/search', methods=['POST'])
def foo():
    global w2v_model
    data = request.json
    if 'query' not in data:
        return {"status": "error"}
    response = json.dumps(processor.search(data['query'], data['fix-misspellings'] if 'fix-misspellings' in data else False, data['use-embeddings'] if 'use-embeddings' in data else False, w2v=w2v_model))
    return response

if __name__ == '__main__':
    w2v_model = KeyedVectors.load_word2vec_format(datapath("/home/dima/models/ArModel100w2v.txt"), binary=False)
    app.run(debug=True, port=5000)