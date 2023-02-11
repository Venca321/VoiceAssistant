
from Modules.functions.functions import *
import os

class Match():
    def match(text, output=False):
        out = Texts.best(f"{os.getcwd()}/Modules/data_processing/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update(timer):
        pass

class Notes():
    def write(text):
        num = 0
        finished = False
        while not finished: #Získá 1. dostupné číslo v sekci [Notes]
            if not str(num) in data.options(f"{os.getcwd()}\\Modules\\data_processing\\Data\\Data.ini", "Notes"):
                option = num
                finished = True
            else: num += 1
        data.write(f"{os.getcwd()}\\Modules\\data_processing\\Data\\Data.ini", "Notes", str(option), text) #Zapíše data

    def read():
        pass

class Records():
    def write(text):
        num = 0
        finished = False
        while not finished: #Získá 1. dostupné číslo v sekci [Records]
            if not str(num) in data.options(f"{os.getcwd()}\\Modules\\data_processing\\Data\\Data.ini", "Records"):
                option = num
                finished = True
            else: num += 1
        data.write(f"{os.getcwd()}\\Modules\\data_processing\\Data\\Data.ini", "Records", str(option), text) #Zapíše data

    def read():
        pass

class To_do_list():
    def write(text):
        num = 0
        finished = False
        while not finished: #Získá 1. dostupné číslo v sekci [To_do_list]
            if not str(num) in data.options(f"{os.getcwd()}\\Modules\\data_processing\\Data\\Data.ini", "To_do_list"):
                option = num
                finished = True
            else: num += 1
        data.write(f"{os.getcwd()}\\Modules\\data_processing\\Data\\Data.ini", "To_do_list", str(option), text) #Zapíše data

    def read():
        pass
