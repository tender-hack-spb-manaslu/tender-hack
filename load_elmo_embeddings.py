from pickle import load

if __name__ == "__main__":
	lemma_embeddings = load(open('lemmas_embeddings.pkl', 'rb'))
	print(lemma_embeddings[list(lemma_embeddings.keys())[0]].shape)
