
from Modules.functions.functions import *
import wikipedia, os

class Wiki():
    def find(text:str):
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

class Google:
    def find():
        pass
