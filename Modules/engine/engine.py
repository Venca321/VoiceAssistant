
from importlib.machinery import SourceFileLoader
from Modules.functions.functions import *
import os

MODULES = data.options(f"{os.getcwd()}/Modules/tester/data/config.ini", "Modules")
imported = {}

for x in MODULES: #Automatický import modulů z listu v /Modules/tester/data/config.ini
    try: imported[x] = SourceFileLoader(x,f'{os.getcwd()}/{data.read(f"{os.getcwd()}/Modules/tester/data/config.ini", "Modules", x)}{x}.py').load_module()
    except: print(f" Error importing {x}")

class Engine():
    def process(text):
        if not text: return
        text = text.lower()
        chars_to_remove = data.options(f"{os.getcwd()}/Modules/engine/data/config.ini", "Characters to remove")
        words_to_remove = data.options(f"{os.getcwd()}/Modules/engine/data/config.ini", "Words to remove")

        for char in chars_to_remove: #Remove znaků z konfigu
            if char in text:
                text = text.replace(char, "")
        
        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if match(words_to_remove, checked_word) > 90:
                text = text.replace(checked_word, "").replace("  ", " ")

        highest_score = 0
        winner = ""
        for i in list(imported.items()): 
            score = int(i[1].Match.match(text))
            if score > highest_score: 
                highest_score = score
                winner = i[1]

        #print(winner)

        #winner.Match.result(text) ???

Engine.process("Ahoj jak se máš? prdel xD")
