
from Modules.functions.functions import *
from geopy.geocoders import Nominatim
from geopy import distance
import requests, json

class Match():
    def match(text:str, output:bool=False):
        """
        Output False: returne procenta nejlepší shody
        Output True: returne výsledek funkce největší shody
        """
        out = Texts.best(f"{os.getcwd()}/Modules/maps/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update(timer:int):
        """
        Updatne data fcí v souboru
        """
        pass

class Distance():
    def air(pos1:str, pos2:str):
        """
        Funkce, která vrátí vzdálenost[km] mezi body vzdušnou čarou
        """
        location1 = Kde_lezi.coords(pos1) #GPS souřadnice míst
        location2 = Kde_lezi.coords(pos2)

        air_distance = int(float(str(distance.distance((location1[0], location1[1]), (location2[0], location2[1]))).replace(" km", ""))*1000)/1000
        
        return air_distance

    def route(pos1:str, pos2:str):
        """
        Funkce, která vrátí vzdálenost[km] a čas[min] mezi body při jízdě po silnici
        """
        location1 = Kde_lezi.coords(pos1) #GPS souřadnice míst
        location2 = Kde_lezi.coords(pos2)

        r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{location1[1]},{location1[0]};{location2[1]},{location2[0]}?overview=false")
        route = (json.loads(r.content)).get("routes")[0]
        distance = int(route["distance"])/1000
        time = int(route["duration"])/60

        return distance, time

class Kde_lezi():
    def coords(pos:str):
        """
        Fuknce, která vrádí souřadnice zadaného místa [lat, long]
        """
        geolocator = Nominatim(user_agent="VoiceAssistant") #Geolocator setup
        location = geolocator.geocode(pos)
        return location.latitude, location.longitude

    def find():
        pass

    def mesto():
        pass

    def stat():
        pass