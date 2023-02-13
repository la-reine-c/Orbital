import pandas as pd
import country_converter as coco
from math import radians, cos, sin, asin, sqrt, atan2
from orbit import satellite
import orbit.tle
from lxml import html
import requests

df = pd.read_csv(r"Orbital\rg_cities1000.csv")
class Coordinates:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def closest_city(self, accuracy=10):
        cities = df.values.tolist()
        citiesSortedByLong = list(sorted(cities, key=lambda x: x[1]))
        citiesSortedByLat = list(sorted(cities, key=lambda x: x[0]))

        searchLat1 = self.lat
        # searchLong1 = -0.13947
        searchLong1 = self.long

        closestCitiesLat = []
        closestLat = min(citiesSortedByLat, key=lambda x: abs(x[0] - searchLat1))
        closestLong = min(citiesSortedByLong, key=lambda x: abs(x[1] - searchLong1))

        minClosestLat = min(citiesSortedByLat, key=lambda x: abs(x[0] - (searchLat1 - accuracy/2)))
        maxClosestLat = min(citiesSortedByLat, key=lambda x: abs(x[0] - (searchLat1 + accuracy/2)))

        minClosestLong = min(citiesSortedByLong, key=lambda x: abs(x[1] - (searchLong1 - accuracy/2)))
        maxClosestLong = min(citiesSortedByLong, key=lambda x: abs(x[1] - (searchLong1 + accuracy/2)))

        closestCitiesList = citiesSortedByLat[citiesSortedByLat.index(minClosestLat): (citiesSortedByLat.index(maxClosestLat) + 1)]
        for city in citiesSortedByLong[citiesSortedByLong.index(minClosestLong): (citiesSortedByLong.index(maxClosestLong) + 1)]:
            closestCitiesList.append(city)


        closestCity = []
        closestDistance = 0

        index = 0

        for city in closestCitiesList:
            cityLat = city[0]
            cityLong = city[1]
            a = self.distance_between_two_coordinates(cityLat, cityLong)
            if index == 0:
                closestDistance = self.distance_between_two_coordinates(cityLat, cityLong)
                city[5] = coco.convert(names=city[5], to='name_short')
                closestCity = [city]
                index += 1
                continue

            if self.distance_between_two_coordinates(cityLat, cityLong) < closestDistance:
                closestDistance = self.distance_between_two_coordinates(cityLat, cityLong)
                city[5] = coco.convert(names=city[5], to='name_short')
                closestCity = [city]
                continue

            if self.distance_between_two_coordinates(cityLat, cityLong) == closestDistance:
                city[5] = coco.convert(names=city[5], to='name_short')
                closestCity.append(city)

        removeDuplicates = {tuple(city) for city in closestCity}

        return removeDuplicates

    def distance_between_two_coordinates(self, lat2, long2):
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(self.long)
        lon2 = radians(long2)
        lat1 = radians(self.lat)
        lat2 = radians(lat2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371

        # calculate the result
        return c * r


class Satellite(Coordinates):

    def __init__(self, catnr):
        self.catnr = catnr
        self.satelliteInfo = satellite(catnr)
        super().__init__(self.satelliteInfo.lat(), self.satelliteInfo.long())
