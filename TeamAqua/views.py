from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
import api.soql
import json

from api.soql import *

# Create your views here.

def indexView(request):
    context = {
            "vehicleAgencies": getUniqueValues("gayt-taic", "agency"),
            "vehicleFuelTypes": getUniqueValues("gayt-taic", "fuel_type")
        }
    return render(request,'TeamAqua/index.html', context=context)


def getUniqueValues(resource, column):
    query = (
        api.soql.SoQL(resource)
        .select([column])
        .groupBy([column])
        .orderBy({column: "ASC"})
    )

    jsonString = query.execute()
    jsonDicts = json.loads(jsonString)
    return [jsonDict[column] for jsonDict in jsonDicts]

