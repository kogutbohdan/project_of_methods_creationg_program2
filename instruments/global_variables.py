#from sentence_transformers import SentenceTransformer
import spacy
import numpy as np

class SpacyEncoder:
    def __init__(self, model_name="en_core_web_md"):
        self.nlp = spacy.load(model_name)

    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        vectors = []

        for doc in self.nlp.pipe(texts):
            vectors.append(doc.vector)

        return np.array(vectors)

sentens_transformer=SpacyEncoder()