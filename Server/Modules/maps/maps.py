
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
        out = Texts.match_in(f"{os.getcwd()}/Modules/maps/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update(timer:int):
        """
        Updatne data fcí v souboru
        """
        pass

class Distance():
    def air(text:str):
        """
        Funkce, která vrátí vzdálenost[km] mezi body vzdušnou čarou
        """
        text = " "+text
        remove_from_input = data.read(f"{os.getcwd()}/Modules/maps/data/config.ini", "vzdalenost_vzduch", "remove_from_input").split(", ")
        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(remove_from_input, checked_word) > 70:
                text = text.replace(f" {checked_word} ", " ").replace("  ", " ")
        if text.startswith(" "): text = text[1:]

        try:
            if " a " in text: text = text.split(" a ")
            elif " do " in text: text = text.split(" do ")
            elif " mezi " in text: text = text.split(" mezi ")
            else: text = text.split(" ")
        except: None

        location1 = Kde_lezi.coords(text[0]) #GPS souřadnice míst
        location2 = Kde_lezi.coords(text[1])
        air_distance = str(int(float(str(distance.distance((location1[0], location1[1]), (location2[0], location2[1]))).replace(" km", ""))*1000)/1000)
        return f"Vzdálenost je {air_distance} km"

    def route(text:str):
        """
        Funkce, která vrátí vzdálenost[km] a čas[min] mezi body při jízdě po silnici
        """

        text = " "+text
        remove_from_input = data.read(f"{os.getcwd()}/Modules/maps/data/config.ini", "vzdalenost_vzduch", "remove_from_input").split(", ")
        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(remove_from_input, checked_word) > 70:
                text = text.replace(f" {checked_word} ", " ").replace("  ", " ")
        if text.startswith(" "): text = text[1:]

        try:
            if " a " in text: text = text.split(" a ")
            elif " do " in text: text = text.split(" do ")
            elif " mezi " in text: text = text.split(" mezi ")
            else: text = text.split(" ")
        except: None

        location1 = Kde_lezi.coords(text[0]) #GPS souřadnice míst
        location2 = Kde_lezi.coords(text[1])
        r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{location1[1]},{location1[0]};{location2[1]},{location2[0]}?overview=false")
        route = (json.loads(r.content)).get("routes")[0]
        distance = int(route["distance"]/2)/1000
        time = int(float(route["duration"])/60*1000/2)/1000
        if time < 120: return f"Vzdálenost je {distance} km, předpokládaný čas {time} min"
        else: return f"Vzdálenost je {distance} km, předpokládaný čas {int(time/60*1000)/1000} h"

class Kde_lezi():
    def coords(pos:str):
        """
        Fuknce, která vrádí souřadnice zadaného místa [lat, long]
        """
        geolocator = Nominatim(user_agent="VoiceAssistant") #Geolocator setup
        location = geolocator.geocode(pos)
        return location.latitude, location.longitude

    def find(text:str):
        """
        Funkce, která rozhodne, zda je text mesto / stát a podle toho callne mesto() / stat()
        """

        remove_from_input = data.read(f"{os.getcwd()}/Modules/maps/data/config.ini", "find", "remove_from_input").split(", ")
        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(remove_from_input, checked_word) > 70:
                text = text.replace(checked_word, "").replace("  ", " ")
        if text.startswith(" "): text = text[1:]

        geolocator = Nominatim(user_agent="VoiceAssistant") #Geolocator setup
        output = str(geolocator.geocode(text)).split(", ")
        if len(output) == 1: return (Kde_lezi.stat(output))
        else: return (Kde_lezi.mesto(output))

    def mesto(text:str):
        """
        Funkce, která vrátí informace o tomto městě
        """
        return f"{text[0]} leží v {text[1]} v {text[2]} na {text[3]} {text[4]}"

    def stat(text:str):
        """
        Funkce, která vrátí informace o tomto státě
        """
        pass