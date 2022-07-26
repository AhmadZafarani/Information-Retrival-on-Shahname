from pathlib import Path

from numpy import dot
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

from .commons import *


class TFIDF:
    def __init__(self, a1: list):
        self.docs = a1
        self.vectorizer = TfidfVectorizer(
            use_idf=True, norm='l2', ngram_range=(1, 1), analyzer='word')
        self.vectorizer.fit_transform(self.docs)

    def forward(self, querry: str, k: int = 10):
        ten_tokens = [0] * k
        ten_scores = [-100] * k

        vector = self.vectorizer.transform([querry])
        b = vector.toarray()
        q1 = querry.split()
        for item in tqdm(self.docs):
            is_common = False
            items = item.split()
            for itemq in q1:
                if itemq in items:
                    is_common = True
            if not is_common:
                continue
            vector = self.vectorizer.transform([item])
            c = vector.toarray()
            if (norm(c[0]) * norm(b[0])) != 0:
                cos_sim = dot(c[0], b[0]) / (norm(c[0]) * norm(b[0]))
                if cos_sim != 0:
                    for i in range(k):
                        if ten_scores[i] < cos_sim:
                            ten_scores[i] = cos_sim
                            ten_tokens[i] = item
                            break
        return ten_tokens


def get_tfidf_query_results(query: str, k: int = 10) -> list:
    cwd = Path(__file__).parent.resolve()
    u = Utils(cwd)
    sen_v2 = u.get_data()
    b1 = TFIDF(sen_v2)
    results = b1.forward(query, k)
    return u.get_beyts_by_mesras(results)
