
import wikipedia, os
from Modules.functions.functions import *

class Match():
    def match(text, output=False):
        return 0

class Data():
    def update(timer):
        pass

class Wiki():
    def find(text):
        remove_from_input = data.read(f"{os.getcwd()}/Modules/web_finder/data/config.ini", "Wiki", "remove_from_input").split(", ")
        remove_from_output = data.read(f"{os.getcwd()}/Modules/web_finder/data/config.ini", "Wiki", "remove_from_output").split(", ")

        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(remove_from_input, checked_word) > 90:
                text = text.replace(checked_word, "").replace("  ", " ")
        if text.startswith(" "): text = text[1:]
        
        wikipedia.set_lang("cs") #Wikipedie CS
        page = wikipedia.search(text) #Stránky
        output = wikipedia.summary(page[0]).split("\n")[0] #Obsah
        
        for checked_word in output.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(remove_from_output, checked_word) > 90:
                output = output.replace(checked_word, "").replace("  ", " ")

        return output

class Google:
    def find():
        pass