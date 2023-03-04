
import datetime, os, random
from Modules.functions.functions import *

class Match():
    def match(user:dict, text:str, output:bool=False):
        """
        Output False: returne procenta nejlepší shody
        Output True: returne výsledek funkce největší shody
        """
        out = Texts.best(f"{os.getcwd()}/Modules/socials/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update(timer:int):
        """
        Updatne data fcí v souboru
        """
        pass

class Socials():
    def ahoj():
        """
        Returne pozdrav
        """
        time = int(datetime.datetime.now().strftime('%H%M'))
        if time < 1000: return "Dobré ráno pane"
        elif time >= 1000 and time <= 1800: return "Dobrý den pane"
        elif time > 1800: return "Dobrý večer pane"
        else: return f"Time error ({time})"

    def jak_se_mas():
        """
        Returne Jak se mám (někdy otázku --bude přidáno)
        """
        pocity = ["Mám se dobře.", "Mám se fajn.", "Jde to.", "Mám se skvěle.", "Dobrý", "Dobře"]
        return random.choice(pocity)

    def help():
        """
        Returne help nabídku
        """
        return " --- Help ---\n Vyhledávání na internetu\n Probíhá vývoj dalších funkcí..."

class Bus():
    pass