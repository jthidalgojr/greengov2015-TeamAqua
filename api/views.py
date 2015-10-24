__author__ = 'Duy'
import json
import requests

from django.http import HttpResponse

from django.views import generic

from .models import portal

class IndexView(generic.ListView):
    """Index Page"""
    model = portal
    context_object_name = 'list_of_resources'
    template_name = 'api/index.html'
    objects = [
            {
                'Name': 'Alternative-Fuel-Station-Locations',
                'link': 'https://greengov.data.ca.gov/resource/sfc3-nf57.json',
                'Resource':'sfc3-nf57',
            },
            {
                'Name': 'CA-State-Fleet-2011-2014',
                'link': 'https://greengov.data.ca.gov/resource/gayt-taic.json',
                'Resource':'gayt-taic',
            }
        ]
    def getResource(self):
        return self.objects


def getList(request):
    objects = [{
                'Name': 'Alternative-Fuel-Station-Locations',
                'link': 'https://greengov.data.ca.gov/resource/sfc3-nf57.json',
                'Resource':'sfc3-nf57',
            },
            {
                'Name': 'CA-State-Fleet-2011-2014',
                'link': 'https://greengov.data.ca.gov/resource/gayt-taic.json',
                'Resource':'gayt-taic',
            }]
    return HttpResponse(json.dumps(objects), content_type='application/json')


def getHydrogen(request):
    query = (
        SoQL("sfc3-nf57")
        .filter("fuel_type_code","HY")
        .select(["station_name", "location_1"])
    )
    return HttpResponse(query.execute())

def getBuildingInformation(request, dept):
    query = (
        SoQL("24pi-kxxa")
        .filter("department", dept)
    )
    return HttpResponse(query.execute())

def getHydrogen(request):
    query = (
        SoQL("sfc3-nf57")
        .filter("fuel_type_code","HY")
        .select(["station_name", "location_1"])
    )
    return HttpResponse(query.execute())

def getBuildingInformation(request, dept):
    query = (
        SoQL("24pi-kxxa")
        .filter("department", dept)
    )
    return HttpResponse(query.execute())

def getElectricVehicles():
    query = (
        api.soql.SoQL("gayt-taic")
        .select(["postal_code", "agency"])
        .filter("fuel_type", "EVC")
    )
    return HttpResponse(query.execute())

def getData(request, resource):
    if( resource == 'gayt-taic'):
        link = 'https://greengov.data.ca.gov/resource/gayt-taic.json?weight_class=Light%20Duty&fuel_type=gas'
    else:
        link = 'https://greengov.data.ca.gov/resource/{0}.json?'.format(resource)
    response = requests.get(link, headers={'X-App-Token': 'eZ54Yp2ubYQAEO2IvzxR7pPQu'})
    return HttpResponse(json.dumps(response.json()))