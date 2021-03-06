__author__ = 'Duy'
import json
import requests
from django.http import HttpResponse
from django.views import generic
from .models import portal
import api.soql

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
        api.soql.SoQL("sfc3-nf57")
        .filter("fuel_type_code","HY")
        .select(["station_name", "location_1"])
    )
    return HttpResponse(query.execute())

def getBuildingInformation(request, dept):
    query = (
        api.soql.SoQL("24pi-kxxa")
        .filter("department", dept)
    )
    return HttpResponse(query.execute())

#what is this for?
def getElectricVehicles():
    query = (
        api.soql.SoQL("gayt-taic")
        .select(["postal_code", "agency"])
        .filter("fuel_type", "EVC")
    )
    return HttpResponse(query.execute())

def findVehiclesForReplacement(request):
    jsonString = showRecommendations(request.GET["agency"], request.GET["total_miles"], request.GET["fuel_type"])
    return HttpResponse(jsonString)

def showRecommendations(request):
    agency = request.GET['agency']
    total_milage = request.GET['total_milage']
    fuel_type = request.GET['fuel_type']

    query = (
        api.soql.SoQL("gayt-taic")
        .select(["vin", "agency", "postal_code"])
        .multiFilter({
            "agency": agency,
            "weight_class": "Light Duty",
            "payload_rating": "0",
            "category": "GROUND",
            "fuel_type": fuel_type
        })
        .where("acquisition_delivery_date <= '2010-01-01T00:00:00'")
        .And("model_year <= '2010'")
        .And("total_miles IS NULL OR total_miles > " + total_milage)
        .And("disposition_method IS NULL")
    )
    return HttpResponse(query.execute(), content_type="application/json")

def findHydrogenStations(request):
    range = request.GET['range']
    zip = request.GET['zip']
    objects = getHydrogen(request)
    return HttpResponse(objects, content_type="application/json")

def getData(request, resource):
    if( resource == 'gayt-taic'):
        link = 'https://greengov.data.ca.gov/resource/gayt-taic.json?weight_class=Light%20Duty&fuel_type=gas'
    else:
        link = 'https://greengov.data.ca.gov/resource/{0}.json?'.format(resource)
    response = requests.get(link, headers={'X-App-Token': 'eZ54Yp2ubYQAEO2IvzxR7pPQu'})
    return HttpResponse(json.dumps(response.json()))

def hydrogenNearAgency(request, agency):
    objects= []
    return HttpResponse(objects)
    #return

def searchHydrogenByDep(request):
    department = request.GET["department_name"]
    return HttpResponse(json.dumps(getHydrogenStationsByDepartment(department)))

def getHydrogenStationsByDepartment(department_name):
    buildingStr = (
        api.soql.SoQL("24pi-kxxa")
        .filter("department_name", department_name)
        .where("location.latitude<1000")
        .And("location.longitude<1000")
        .select(["location.latitude","location.longitude"])
    ).execute()

    buildings = json.loads(buildingStr)
    coordinateList = [(float(building["sub_col_location_latitude"]),float(building["sub_col_location_longitude"]))
                      for building in buildings]

    kmPerLong = 111.32*0.766044443
    kmPerLat = 110.574
    milesPerKm = 1.6
    limitInMiles = 30.0
    squareCoordLimit = (limitInMiles/milesPerKm/kmPerLat)*(limitInMiles/milesPerKm/kmPerLong)

    allStations = json.loads(
        api.soql.SoQL("sfc3-nf57")
        .filter("fuel_type_code", "HY")
        .where("location_1.latitude<1000")
        .And("location_1.longitude<1000")
        .execute()
    )

    return list(filter(lambda station: isCloseEnough(station, coordinateList, squareCoordLimit), allStations))

def isCloseEnough(station, coordinateList, dist):
    for coordinates in coordinateList:
        if (
            (float(station["location_1"]["latitude"])-coordinates[0])*(float(station["location_1"]["latitude"])-coordinates[0])+
            (float(station["location_1"]["longitude"])-coordinates[1])*(float(station["location_1"]["longitude"])-coordinates[1])
            < dist
        ):
            return True
    return False