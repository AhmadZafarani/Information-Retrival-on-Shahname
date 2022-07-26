from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('retrival/<str:retrival_type>/', retrival, name='retrival'),
    path('clustering/', clustering, name='clustering'),
    path('classification/', classification, name='classification'),
    path('elastic/', elastic, name='elastic'),
    path('link_analyze/', link_analyze, name='link_analyze'),
]
