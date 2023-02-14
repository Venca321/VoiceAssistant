
from Modules.functions.functions import *
from geopy.geocoders import Nominatim
from geopy import distance
import wikipedia, os, requests, json


class Wiki():
    def find(text):
        """
        Najde v textu klíčová slova, které najde na wikipedii, pokud dosáhne dostatečné shody, vrátí to
        text = string
        """
        remove_from_input = data.read(f"{os.getcwd()}/Modules/web_finder/data/config.ini", "Wiki", "remove_from_input").split(", ")
        remove_from_output = data.read(f"{os.getcwd()}/Modules/web_finder/data/config.ini", "Wiki", "remove_from_output").split(", ")

        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(remove_from_input, checked_word) > 90:
                text = text.replace(checked_word, "").replace("  ", " ")
        if text.startswith(" "): text = text[1:]
        
        wikipedia.set_lang("cs") #Wikipedie CS
        page = wikipedia.search(text) #Stránky
        if Texts.match([page[0]], text) >= 80: #Checkout zda title stránky má s texten shodu větší, než 80%
            output = wikipedia.summary(page[0]).split("\n")[0] #Obsah
            
            for checked_word in output.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
                if Texts.match(remove_from_output, checked_word) > 90:
                    output = output.replace(checked_word, "").replace("  ", " ")

            return output

class Map():
    def air_distance(pos1, pos2):
        geolocator = Nominatim(user_agent="VoiceAssistant") #Geolocator setup
        location1 = geolocator.geocode(pos1) #GPS souřadnice míst
        location2 = geolocator.geocode(pos2)

        air_distance = int(float(str(distance.distance((location1.latitude, location1.longitude), (location2.latitude, location2.longitude))).replace(" km", ""))*1000)/1000
        
        return air_distance

    def route_distance(pos1, pos2):
        geolocator = Nominatim(user_agent="VoiceAssistant") #Geolocator setup
        location1 = geolocator.geocode(pos1) #GPS souřadnice míst
        location2 = geolocator.geocode(pos2)

        r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{location1.longitude},{location1.latitude};{location2.longitude},{location2.latitude}?overview=false")
        route = (json.loads(r.content)).get("routes")[0]
        distance = int(route["distance"])/1000
        time = int(route["duration"])/60

        return distance, time

class Google:
    def find():
        pass
