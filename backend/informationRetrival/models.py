from .logic.boolean import get_boolean_query_results
from .logic.clustering import get_cluster_number_for_query
from .logic.query_expansion import query_expansion
from .logic.fasttext import get_fasttext_query_results
from .logic.tf_idf import get_tfidf_query_results
from .logic.classification import get_classification_story_for_query


def boolean(query: str, k: int) -> dict:
    result = {}
    expanded_query = query_expansion(query)
    result["expanded_query"] = expanded_query
    answers = get_boolean_query_results(query, k)
    result["answers"] = normalize(answers)
    expanded_answers = get_boolean_query_results(expanded_query, k)
    result["expanded_answers"] = normalize(expanded_answers)
    return result


def tfidf(query: str, k: int) -> dict:
    result = {}
    expanded_query = query_expansion(query)
    result["expanded_query"] = expanded_query
    answers = get_tfidf_query_results(query, k)
    result["answers"] = normalize(answers)
    expanded_answers = get_tfidf_query_results(expanded_query, k)
    result["expanded_answers"] = normalize(expanded_answers)
    return result


def fasttext(query: str, k: int) -> dict:
    result = {}
    expanded_query = query_expansion(query)
    result["expanded_query"] = expanded_query
    answers = get_fasttext_query_results(query, k)
    result["answers"] = normalize(answers)
    expanded_answers = get_fasttext_query_results(expanded_query, k)
    result["expanded_answers"] = normalize(expanded_answers)
    return result


def transformers(query: str, k: int) -> list:
    pass


def clustering(query: str) -> dict:
    result = {}
    expanded_query = query_expansion(query)
    result["expanded_query"] = expanded_query
    nearest_cluster = get_cluster_number_for_query(query) + 1
    result["nearest_cluster"] = nearest_cluster
    nearest_expanded_cluster = get_cluster_number_for_query(expanded_query) + 1
    result["nearest_expanded_cluster"] = nearest_expanded_cluster
    return result


def classification(query: str) -> str:
    result = {}
    expanded_query = query_expansion(query)
    result["expanded_query"] = expanded_query
    label = get_classification_story_for_query(query)
    result["label"] = label
    expanded_label = get_classification_story_for_query(expanded_query)
    result["expanded_label"] = expanded_label
    return result


def elastic(query: str, k: int) -> list:
    pass


def link_analyze(query: str) -> int:
    names = {}
    return names.get(query, "")


def normalize(answers: list) -> list:
    result = []
    for answer in answers:
        result.append(answer.replace("####", "\t\t\t"))
    return result