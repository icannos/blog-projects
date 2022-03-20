import geopy
from geopy import Nominatim
from sys import argv
import pandas as pd


if len(argv) != 2:
    print("get_cities csv path")
    exit(1)

data = pd.read_csv(argv[1], sep=";", names=["city", "dinner_b", "dinner_e"])

geolocator = Nominatim(user_agent="tutorial")

lat = []
lon = []
for city in data["city"]:
    location = geolocator.geocode(city)
    print(city)
    lat.append(location.latitude)
    lon.append(location.longitude)


data["lat"] = lat
data["lon"] = lon

data.to_csv("cities_wcoords.csv", sep=";", index=False)
