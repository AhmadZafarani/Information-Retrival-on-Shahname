from elasticsearch import Elasticsearch


class Elastic:
    def forward(self, query: str, k: int = 10) -> list:
        client = Elasticsearch("http://localhost:9200")
        search_param = {
            "match": {
                "Beyt": "" + query + ""
            }
        }

        beyts = []
        response = client.search(
            index="shahnameh",  query=search_param, size=k)
        for hit in response['hits']['hits']:
            beyts.append(hit["_source"]["Beyt"].replace("##", "***"))
        return beyts


def get_elastic_search_query_results(query: str, k: int = 10) -> list:
    b1 = Elastic()
    results = b1.forward(query, k)
    return results
