
import os

while True:
    input1 = input("Mohu instalovat potřebné knihovny z requirements.txt (Y/n)? ").lower()
    if input1 == "y" or input1 == "": break
    elif input1 == "n": exit()
    
os.system('pip install -r requirements.txt') #Instalace requirements.txt

import configparser

while True:
    input4 = input("Chcete použít vyhledávání informací online (Y/n)? ").lower()
    if input4 == "y" or input4 == "": break
    elif input4 == "n": 
        data = configparser.ConfigParser(allow_no_value=True)
        data.read("Data/config.ini")
        data.set("Settings", "wiki_finder_online", "False")
        with open("Data/config.ini", "w") as configfile: data.write(configfile) #Uložení
        print("Než budete pokračovat, postupujte podle dokumentace a stáhněte si wikidata")
        exit()

data = configparser.ConfigParser(allow_no_value=True)
data.read("Data/config.ini")
data.set("Settings", "wiki_finder_online", "True")
with open("Data/config.ini", "w") as configfile: data.write(configfile) #Uložení

print("Instalace dokončena")