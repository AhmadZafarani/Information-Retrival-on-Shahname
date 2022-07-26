import codecs
import random
from pathlib import Path

import numpy as np
from numpy import dot
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

from .commons import Utils


class TFIDF:
    def __init__(self, a1: list):
        self.docs = a1
        self.vectorizer = TfidfVectorizer(
            use_idf=True, norm='l2', ngram_range=(1, 1), analyzer='word')
        self.vectorizer.fit_transform(self.docs)
        cwd = Path(__file__).parent.resolve()
        sw = cwd / Path('stopwords.txt')
        with codecs.open(sw, 'r', 'utf-8') as f:
            ls = f.readlines()
        self.stopwords = [x.strip() for x in ls]

    def forward(self, querry: str, k=10, is_vector=False, words=[]):
        ten_tokens = [0] * k
        ten_scores = [-100] * k

        if not is_vector:
            vector = self.vectorizer.transform([querry])
            b = vector.toarray()
            q1 = querry.split()
        else:
            vector = querry
            b = [vector.tolist()]
            q1 = words

        NR = []
        for item in tqdm(self.docs):
            is_common = False
            items = item.split()
            for itemq in q1:
                if itemq in items:
                    is_common = True
            if not is_common:
                NR.append(item)
                continue
            vector = self.vectorizer.transform([item])
            c = vector.toarray()
            if (norm(c[0])*norm(b[0])) != 0:
                cos_sim = dot(c[0], b[0])/(norm(c[0])*norm(b[0]))
                if cos_sim != 0:
                    for i in range(k):
                        if ten_scores[i] < cos_sim:
                            ten_scores[i] = cos_sim
                            ten_tokens[i] = item
                            break
                    for i in range(k):
                        for j in range(i, k):
                            if ten_scores[i] > ten_scores[j]:
                                ten_scores[i], ten_scores[j] = ten_scores[j], ten_scores[i]
                                ten_tokens[i], ten_tokens[j] = ten_tokens[j], ten_tokens[i]
        return ten_tokens, NR

    def query_expansion(self, query: str)->list:
        R, NR = self.forward(query)
        NR = random.sample(NR, 10)
        R_vecs = []
        NR_vecs = []
        words = []
        for item in R:
            items = item.split()
            for itemq in items:
                if itemq not in self.stopwords:
                    words.append(itemq)
            vector = self.vectorizer.transform([item])
            c = np.array(vector.toarray()[0])
            R_vecs.append(c)
        words = random.sample(words, 6)
        for oo in query.split():
            words.append(oo)
        R_vecs = np.array(R_vecs)
        R_mean = np.mean(R_vecs, axis=0)
        for item in NR:
            vector = self.vectorizer.transform([item])
            c = np.array(vector.toarray()[0])
            NR_vecs.append(c)
        NR_vecs = np.array(NR_vecs)
        out1, _ = self.forward(query, 1)
        vector = self.vectorizer.transform(out1)
        a, _ = self.forward(R_mean, 1, True, words)
        return a


def query_expansion(query: str) -> str:
    cwd = Path(__file__).parent.resolve()
    u = Utils(cwd)
    sen_v2 = u.get_data()
    query_expander = TFIDF(sen_v2)
    return query_expander.query_expansion(query)[0].strip().replace('\n', '')
