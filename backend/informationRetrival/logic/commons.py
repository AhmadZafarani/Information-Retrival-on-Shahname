from pathlib import Path

import numpy as np
from gensim.models.keyedvectors import KeyedVectors

from .fasttext import FastText


class Utils:
    def __init__(self, cwd: Path) -> None:
        with open(cwd / Path('sen_v2.txt'), 'r', encoding='utf-8') as f:
            self.data = f.readlines()

    def get_data(self) -> list:
        return self.data

    def get_beyts_by_mesras(self, mesras: list) -> list:
        beyts = []
        for mesra in mesras:
            idx = self.data.index(mesra)
            if idx % 2 == 0:
                beyt = mesra + "####" + self.data[idx + 1]
            else:
                beyt = self.data[idx - 1] + "####" + mesra
            beyts.append(beyt.strip().replace('\n', ''))
        return beyts


class QueryExpansion(FastText):
    def __init__(self, fasttext_vectors: np.array, word_vectors: KeyedVectors, a1: list, dims: int = 100):
        self.fasttext_vectors = fasttext_vectors
        super().__init__(word_vectors, a1, dims)

    def query_expansion(self, query: str) -> str:
        number_of_related_queries = 100
        vector = self.get_fasttext(query)
        vector /= np.linalg.norm(vector)
        final_vector = np.matmul(self.fasttext_vectors, np.transpose(vector))
        R = np.array(final_vector).argsort()[-number_of_related_queries:][::-1]
        NR = np.array(final_vector).argsort()[:number_of_related_queries][::-1]
        R_mean = np.mean(self.fasttext_vectors[R])
        NR_mean = np.mean(self.fasttext_vectors[NR])
        expanded_vector = vector + 1.5 * R_mean - 0.4 * NR_mean
        expanded_vector /= np.linalg.norm(expanded_vector)
        R_expanded = np.array(final_vector).argsort()[-1:][::-1]
        expanded_query = self.docs[R_expanded]
        return expanded_query


def query_expansion(query: str) -> str:
    cwd = Path(__file__).parent.resolve()
    vector_file_path = cwd / Path('fasttext_vec_file.vec')
    word_vectors = KeyedVectors.load_word2vec_format(vector_file_path)
    u = Utils(cwd)
    sen_v2 = u.get_data()
    fasttext_vectors = np.loadtxt(cwd / Path('fasttext_vectors.txt'))
    nan_indexes = []
    for i in range(len(fasttext_vectors)):
        if np.isnan(fasttext_vectors[i]).any():
            nan_indexes.append(i)
    fasttext_vectors = np.delete(fasttext_vectors, nan_indexes, axis=0)
    sen_v2 = np.delete(sen_v2, nan_indexes, axis=0)
    query_expander = QueryExpansion(fasttext_vectors, word_vectors, sen_v2)
    return query_expander.query_expansion(query)[0].strip().replace('\n', '')
