from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
import api.soql
import json

from api.soql import *

# Create your views here.

def indexView(request):
    context = {
            "vehicleAgencies": getUniqueValues("gayt-taic", "agency", "max(postal_code)"),
            "vehicleFuelTypes": getUniqueValues("gayt-taic", "fuel_type", "max(postal_code)")
        }
    return render(request,'TeamAqua/index.html', context=context)


def getUniqueValues(resource, column, aggregate):
    query = (
        api.soql.SoQL(resource)
        .select([column, aggregate])
        .groupBy([column])
        .orderBy({column: "ASC"})
    )

    jsonString = query.execute()
    return json.loads(jsonString)

