__author__ = 'Duy'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<resource>.*)/getData/$', views.getData, name='getData'),
    url(r'^getList/$', views.getList, name='getList'),
]