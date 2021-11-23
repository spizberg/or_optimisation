from typing import List
from weakref import WeakSet


class Flight:
    def __init__(self, id: int, costs_list: List[str]):
        self.id = id
        self.costs_list = []
        for cost in costs_list:
            self.costs_list.append(int(cost))
        self.made = False
        self.plane = []
        self.destinations = WeakSet()
        self.correspondences = WeakSet()

    def doFlight(self):
        self.made = True

    def addDestination(self, flight):
        self.destinations.add(flight)

    def getNumberOfDestinations(self):
        return len(self.destinations)

    def getMinimumPlaneCost(self, planes_done):
        minimum = {"id": None, "value":float('inf')}
        for index, cost in enumerate(self.costs_list):
            if cost < minimum["value"] and planes_done[index]==False:
                minimum["id"] = index
                minimum["value"] = cost
        return minimum["id"]

    def getMinimumDestination(self, plane):
        minimum = {"object": None, "value": float('inf')}
        for flight in list(self.destinations):
            if flight.costs_list[plane.id - 1] < minimum["value"]:
                minimum["object"] = flight
                minimum["value"] = flight.costs_list[plane.id - 1]
        return minimum["object"]
    
    def __str__(self):
        return "Vol d'id {}".format(self.id)

class Plane:
    def __init__(self, id: int):
        self.id = id
        self.done = False
        self.rotation = []

    def populateRotation(self, flight: Flight):
        self.rotation.append(flight)

    def getNumberOfFlights(self):
        return len(self.rotation)

    def getFlights(self):
        for flight in self.rotation:
            print(flight.id)


class Correspondence:
    def __init__(self, id: int, origin: Flight, destination: Flight, maintenace_base: bool, duration: int):
        self.id = id
        self.origin = origin
        self.destination = destination
        self.maintenance_base = maintenace_base
        self.duration = duration
        self.used = False
        self.dropped = False
        self.plane = None

    def makeCorrespondence(self, plane: Plane):
        self.plane = plane
        self.used = True

    def dropCorrespondence(self):
        self.dropped = True

    def __str__(self):
        return "Correspondance numéro {} avec le vol {} au départ et le vol {} à la destination. Il est {} ou {} ".format(
            self.id, self.origin.id, self.destination.id, self.used, self.dropped)