
from importlib.machinery import SourceFileLoader
from Modules.functions.functions import *
from Modules.web_finder import web_finder
import os, datetime

LOGS_LIMIT = 25
MODULES = data.options(f"{os.getcwd()}/Modules/tester/data/config.ini", "Modules")
WEB_WIKI = str(data.read(f"{os.getcwd()}/Data/config.ini", "Settings", "wiki_finder_online"))
imported = {}

for x in MODULES: #Automatický import modulů z listu v /Modules/tester/data/config.ini
    try: imported[x] = SourceFileLoader(x,f'{os.getcwd()}/{data.read(f"{os.getcwd()}/Modules/tester/data/config.ini", "Modules", x)}{x}.py').load_module()
    except: print(f" Error importing {x}")

class Engine():
    def process(user:dict, text:str):
        """
        Zpracuje požadavek text[str] a vrátí odpověď[str], nebo nic, pokud odpověď není
        """
        if not text: return
        origo_text = text
        if text == "9H9k2bm!&64iNoerHuwB@HkON": return "nNq8j3ma15G^KXaV33Ma*W^Rj"
        text = text.lower()
        chars_to_remove = data.options(f"{os.getcwd()}/Modules/engine/data/config.ini", "Characters to remove")
        words_to_remove = data.options(f"{os.getcwd()}/Modules/engine/data/config.ini", "Words to remove")

        for char in chars_to_remove: #Remove znaků z konfigu
            if char in text:
                text = text.replace(char, "")
        
        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(words_to_remove, checked_word) > 90:
                text = text.replace(checked_word, "").replace("  ", " ")

        highest_score = 0
        winner = ""
        for i in list(imported.items()): 
            score = int(i[1].Match.match(user, text))
            if score > highest_score: 
                highest_score = score
                winner = i[1]

        if highest_score > 85: output = winner.Match.match(user, text, True) #Pokud by byla potřeba nějaká úprava textu
        elif WEB_WIKI == "True":  output = web_finder.Wiki.web_find(text)
        else: output = web_finder.Wiki.wikidata_find(text)

        data.write(f"{os.getcwd()}/Modules/engine/data/.userdata/{user['username']}.ini", "Log", datetime.datetime.now().strftime("%d/%m/%Y_%H/%M/%S/%f"), Userdata.encode(f"{origo_text}", user['password']))
        logs = data.options(f"{os.getcwd()}/Modules/engine/data/.userdata/{user['username']}.ini", "Log")
        if len(logs) >= LOGS_LIMIT:
            for i in range(len(logs)-(LOGS_LIMIT-1)):
                data.remove_option(f"{os.getcwd()}/Modules/engine/data/.userdata/{user['username']}.ini", "Log", logs[i])

        return output