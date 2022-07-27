from pathlib import Path

import numpy as np
import torch
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer

from .commons import Utils


class Transformer:
    def __init__(self, a1: list):
        self.docs = a1
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer()
        self.model.to(device)

    def forward(self, querry, cwd: Path, k=10):
        ten_tokens = [0] * k
        ten_scores = [-100] * k
        vocab_error = 0
        b = self.model.encode(querry)

        all_vectors = np.loadtxt(cwd / Path('all_vec.out'), delimiter=",")
        for o in range(len(all_vectors)):
            try:
                c = all_vectors[o]
                if norm(c) * norm(b) != 0:
                    cos_sim = dot(c, b) / (norm(c) * norm(b))
                    if cos_sim != 0:
                        for i in range(k):
                            if ten_scores[i] < cos_sim:
                                ten_scores[i] = cos_sim
                                ten_tokens[i] = self.docs[o]
                                break
                        for i in range(k):
                            for j in range(i, k):
                                if ten_scores[i] > ten_scores[j]:
                                    ten_scores[i], ten_scores[j] = ten_scores[j], ten_scores[i]
                                    ten_tokens[i], ten_tokens[j] = ten_tokens[j], ten_tokens[i]

            except Exception:
                vocab_error += 1
                continue
        return ten_tokens


def get_transformers_answers_for_query(query: str, k: int = 10) -> str:
    cwd = Path(__file__).parent.resolve()
    u = Utils(cwd)
    sen_v2 = u.get_data()

    trans = Transformer(sen_v2)
    trans.model = trans.model.load(cwd / Path('saved_transformers_model'))
    results = trans.forward(query, cwd, k)
    return u.get_beyts_by_mesras(results)
