
from Modules.functions.functions import *
import os

class Match():
    def match(user:dict, text:str, output:bool=False):
        """
        Output False: returne procenta nejlepší shody
        Output True: returne výsledek funkce největší shody
        """
        out = Texts.match_in(f"{os.getcwd()}/Modules/data_processing/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update(timer:int):
        """
        Updatne data fcí v souboru
        """
        pass

class Notes():
    def write(user:dict, text:str):
        """
        Zapíše poznámky
        """
        num = 0
        finished = False
        while not finished: #Získá 1. dostupné číslo v sekci [Notes]
            if not str(num) in data.options(f"{os.getcwd()}/Modules/data_processing/data/.userdata/{user['username']}.ini", "Notes"):
                option = num
                finished = True
            else: num += 1
        data.write(f"{os.getcwd()}/Modules/data_processing/data/.userdata/{user['username']}.ini", "Notes", str(option), Userdata.encode(text, user["password"])) #Zapíše data

    def read(user:dict):
        pass

class Records():
    def write(user:dict, text:str):
        """
        Zapíše rekord
        """
        num = 0
        finished = False
        while not finished: #Získá 1. dostupné číslo v sekci [Records]
            if not str(num) in data.options(f"{os.getcwd()}/Modules/data_processing/data/.userdata/{user['username']}.ini", "Records"):
                option = num
                finished = True
            else: num += 1
        data.write(f"{os.getcwd()}/Modules/data_processing/data/.userdata/{user['username']}.ini", "Records", str(option), Userdata.encode(text, user["password"])) #Zapíše data

    def read(user:dict):
        pass

class To_do_list():
    def write(user:dict, text:str):
        """
        Zapíše věc do to do listu
        """
        num = 0
        finished = False
        while not finished: #Získá 1. dostupné číslo v sekci [To_do_list]
            if not str(num) in data.options(f"{os.getcwd()}/Modules/data_processing/data/.userdata/{user['username']}.ini", "To_do_list"):
                option = num
                finished = True
            else: num += 1
        data.write(f"{os.getcwd()}/Modules/data_processing/data/.userdata/{user['username']}.ini", "To_do_list", str(option), Userdata.encode(text, user["password"])) #Zapíše data

    def read(user:dict):
        pass
