
from Modules.functions.functions import *
from geopy.geocoders import Nominatim
from geopy import distance
import requests, json

class Match():
    def match(text, output=False):
        out = Texts.best(f"{os.getcwd()}/Modules/maps/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update():
        pass

class Distance():
    def air(pos1, pos2):
        geolocator = Nominatim(user_agent="VoiceAssistant") #Geolocator setup
        location1 = geolocator.geocode(pos1) #GPS souřadnice míst
        location2 = geolocator.geocode(pos2)

        air_distance = int(float(str(distance.distance((location1.latitude, location1.longitude), (location2.latitude, location2.longitude))).replace(" km", ""))*1000)/1000
        
        return air_distance

    def route(pos1, pos2):
        geolocator = Nominatim(user_agent="VoiceAssistant") #Geolocator setup
        location1 = geolocator.geocode(pos1) #GPS souřadnice míst
        location2 = geolocator.geocode(pos2)

        r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{location1.longitude},{location1.latitude};{location2.longitude},{location2.latitude}?overview=false")
        route = (json.loads(r.content)).get("routes")[0]
        distance = int(route["distance"])/1000
        time = int(route["duration"])/60

        return distance, time

class Kde_lezi():
    def find():
        pass

    def mesto():
        pass

    def stat():
        pass