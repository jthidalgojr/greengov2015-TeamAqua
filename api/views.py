__author__ = 'Duy'
import json
from django.http import HttpResponse

from django.views import generic

class IndexView(generic.ListVIew):
    """Index Page"""
    template_name = 'api/index.html'

def getList(request):
    objects = [dict(file=f) for f in os.listdir('polls/dump/')]

    return HttpResponse(json.dumps(objects), content_type='application/json')

def getData(request, resource):
    f = open('polls/dump/{0}.json'.format(resource), 'r')
    data = json.loads(f.read())
    return HttpResponse(json.dumps(data))