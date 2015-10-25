__author__ = 'James'

import urllib.parse
import http.client

class SoQL:
    def __init__(self, resourceId):
        self.resourceId = resourceId
        self.params = {}
        #max limit by default
        self.limit(50000)

    def _buildRequest(self):
        return"/resource/" + self.resourceId + ".json?" + urllib.parse.urlencode(self.params)

    #returns json string from query
    def execute(self):
        conn = http.client.HTTPSConnection('greengov.data.ca.gov')
        conn.request("GET", self._buildRequest(), headers={"X-App-Token": "eZ54Yp2ubYQAEO2IvzxR7pPQu"})
        return conn.getresponse().read().decode("utf-8")

    def filter(self, column, value):
        self.params[column] = value
        return self

    def multiFilter(self, filters):
        self.params.update(filters)
        return self

    def select(self, columns):
        self.params["$select"] = ",".join(columns)
        return self

    def where(self, condition):
        self.params["$where"] = condition
        return self

    #"and" is reserved
    def And(self, condition):
        self.params["$where"] += " AND " + condition
        return self

    #e.g. {"total_miles": "DESC"}
    def orderBy(self, columns):
        columnsFormatted = [k+" "+v for k, v in columns.items()]
        self.params["$order"] = ",".join(columnsFormatted)
        return self

    def limit(self, lim):
        self.params["$limit"] = str(lim)
        return self

    def groupBy(self, columns):
        self.params["$group"] = ",".join(columns)
        return self


def test():
    query = (
        SoQL("aazw-6wcw")
        .filter("disposed","No")
        .multiFilter({"fuel_type": "EVC"})
        .orderBy({"total_miles": "DESC"})
        .select(["vin", "agency"])
    )
    print(query._buildRequest())
    print(query.execute())
