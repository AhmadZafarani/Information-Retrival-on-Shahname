from pathlib import Path

import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from hazm import word_tokenize
from numpy.linalg import norm


def get_fastext_average(mesra: str, cwd: Path) -> np.array:
    vector_file_path = cwd / Path('clustering_vec_file.vec')
    word_vectors = KeyedVectors.load_word2vec_format(vector_file_path)
    vector_sum = np.zeros(200)
    num = 0
    words = word_tokenize(mesra)
    for word in words:
        try:
            vector_sum += word_vectors[word]
            num += 1
        except:
            continue
    return vector_sum / num


def get_cluster_number_for_query(query: str) -> int:
    cwd = Path(__file__).parent.resolve()
    centers_file_path = cwd / Path('cluster_centers.txt')
    centers = np.loadtxt(centers_file_path, dtype=float)
    embedded_query = get_fastext_average(query, cwd)
    max_similarity = -1
    final_center = -1
    for i in range(len(centers)):
        center = centers[i]
        similarity = np.dot(embedded_query, center) / \
            (norm(center) * norm(embedded_query))
        if similarity > max_similarity:
            max_similarity = similarity
            final_center = i
    return final_center
