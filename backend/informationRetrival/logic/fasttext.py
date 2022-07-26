from pathlib import Path

import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from numpy import dot
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

from .commons import Utils


class FastText:
    def __init__(self, word_vectors: KeyedVectors, a1: list, dims=100):
        self.word_vectors = word_vectors
        self.docs = a1
        self.dims = dims
        self.vectorizer = TfidfVectorizer(
            use_idf=True, norm='l1', ngram_range=(1, 1), analyzer='word')
        self.vectorizer.fit_transform(self.docs)
        self.strings = [].extend(self.vectorizer.get_feature_names())
        string = ' '.join(self.vectorizer.get_feature_names())
        self.vector = self.vectorizer.transform([string])
        self.vector = self.vector.toarray()

    def get_fastext_average(self, mesra: str) -> np.array:
        counter = 0
        vector_sum = np.zeros(self.dims)
        words = mesra.split(' ')
        for word in words:
            try:
                vector_sum += self.word_vectors[word]
                counter += 1
            except:
                continue
            vector_sum /= counter
        return vector_sum

    def get_fasttext(self, mesra: str) -> np.array:
        return self.get_fastext_average(mesra)

    def forward(self, query: str, k: int = 10) -> list:
        ten_tokens = [0] * k
        ten_scores = [-100] * k
        b = self.get_fasttext(query)

        for item in tqdm(self.docs):
            try:
                c = self.get_fasttext(item)
                if (norm(c) * norm(b)) != 0:
                    cos_sim = dot(c, b) / (norm(c) * norm(b))
                    if cos_sim != 0:
                        for i in range(k):
                            if ten_scores[i] < cos_sim:
                                ten_scores[i] = cos_sim
                                ten_tokens[i] = item
                                break
            except Exception:
                continue

        for i in range(len(ten_scores)):
            for j in range(len(ten_scores)):
                if ten_scores[i] > ten_scores[j]:
                    ten_scores[i], ten_scores[j] = ten_scores[j], ten_scores[i]
                    ten_tokens[i], ten_tokens[j] = ten_tokens[j], ten_tokens[i]

        return ten_tokens


def get_fasttext_query_results(query: str, k: int = 10) -> list:
    cwd = Path(__file__).parent.resolve()
    u = Utils(cwd)
    sen_v2 = u.get_data()
    vector_file_path = cwd / Path('vec_file.vec')
    word_vectors = KeyedVectors.load_word2vec_format(vector_file_path)
    fasttext1_2 = FastText(word_vectors, sen_v2)
    nearest_mesras = fasttext1_2.forward(query, k)
    return u.get_beyts_by_mesras(nearest_mesras)
