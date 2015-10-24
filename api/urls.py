__author__ = 'Duy'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.IndexView.as_view(), name='index'),
    url(r'^(?P<resource>.*)/getData/$', views.getData, name='getData'),
    url(r'^getList/$', views.getList, name='getList'),
]