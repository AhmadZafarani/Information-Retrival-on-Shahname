from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseBadRequest)
from django.shortcuts import render

from . import models


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'informationRetrival/index.html')


def retrival(request: HttpRequest, retrival_type: str) -> HttpResponse:
    allowed_types = {'boolean': models.boolean, 'tfidf': models.tfidf,
                     'fasttext': models.fasttext, 'transformers': models.transformers}
    if retrival_type not in allowed_types:
        raise Http404("Retrival Type does not exist")

    query = request.GET.get('query', None)
    if query is None:
        return HttpResponseBadRequest("`query` argument not found in the request")

    k = request.GET.get('k', None)
    if k is None:
        return HttpResponseBadRequest("`k` argument not found in the request")
    k = int(k)
    result = allowed_types[retrival_type](query, k)
    return render(request, 'informationRetrival/retrival.html', context={'result': result})


def clustering(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('query', None)
    if query is None:
        return HttpResponseBadRequest("`query` argument not found in the request")

    result = models.clustering(query)
    return render(request, 'informationRetrival/clustering.html', context={'result': result})


def classification(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('query', None)
    if query is None:
        return HttpResponseBadRequest("`query` argument not found in the request")

    result = models.classification(query)
    return render(request, 'informationRetrival/classification.html',
                  context={'result': result})


def elastic(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('query', None)
    if query is None:
        return HttpResponseBadRequest("`query` argument not found in the request")

    k = request.GET.get('k', None)
    if k is None:
        return HttpResponseBadRequest("`k` argument not found in the request")
    k = int(k)
    result = models.elastic(query, k)
    return render(request, 'informationRetrival/elastic.html',
                  context={'result': result})


def link_analyze(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('query', None)
    if query is None:
        return HttpResponseBadRequest("`query` argument not found in the request")

    result = models.link_analyze(query)
    return render(request, 'informationRetrival/link_analyze.html',
                  context={'result': result})
