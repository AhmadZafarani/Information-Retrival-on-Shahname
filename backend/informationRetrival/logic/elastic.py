from pathlib import Path

from elasticsearch import Elasticsearch
from .commons import *


class Elastic:
    def __init__(self, a1: list):
        self.docs = a1

    def forward(self, query: str, k: int = 10) -> list:
        client = Elasticsearch("http://localhost:9200")
        search_param = {
            "match": {
                "mesra": "" + query + ""
            }
        }

        mesras = []
        response = client.search(
            index=self.docs,  query=search_param, size=k)
        for hit in response['hits']['hits']:
            mesras.append(hit["_source"])
        return mesras


def get_elastic_search_query_results(query: str, k: int = 10) -> list:
    cwd = Path(__file__).parent.resolve()
    u = Utils(cwd)
    sen_v2 = u.get_data()
    b1 = Elastic(sen_v2)
    results = b1.forward(query, k)
    return u.get_beyts_by_mesras(results)
