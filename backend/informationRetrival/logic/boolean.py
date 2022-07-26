from pathlib import Path

from tqdm import tqdm

from informationRetrival.logic.commons import *


class Boolean:
    def __init__(self, a1: list):
        self.docs = a1

    def forward(self, querry: str, k: int = 10):
        result = []
        for item in tqdm(self.docs):
            status = True
            items = item.split()
            for itemq in querry.split():
                if itemq not in items:
                    status = False
                    break
            if status:
                result.append(item)
        return result[:k]


def get_boolean_query_results(query: str, k: int = 10) -> list:
    cwd = Path(__file__).parent.resolve()
    u = Utils(cwd)
    sen_v2 = u.get_data()
    b1 = Boolean(sen_v2)
    results = b1.forward(query, k)
    return u.get_beyts_by_mesras(results)
