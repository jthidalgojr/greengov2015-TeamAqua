__author__ = 'Duy'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.indexView, name='index'),
]
