
import os

while True:
    input1 = input("Mohu instalovat potřebné knihovny z requirements.txt (Y/n)? ").lower()
    if input1 == "y" or input1 == "": break
    elif input1 == "n": exit()
    
os.system('pip install -r requirements.txt') #Instalace requirements.txt

import configparser

while True:
    input1 = input("Chcete použít ngrok pro hosting (budete ho muset manuálně instalovat) (Y/n)? ").lower()
    if input1 == "y" or input1 == "": 
        data = configparser.ConfigParser(allow_no_value=True)
        data.read("Data/config.ini")
        data.set("Settings", "nrgok", "True")
        with open("Data/config.ini", "w") as configfile: data.write(configfile) #Uložení
        print("Prosím, než spustíte main.py, ujistěte se, že máte nainstalovaný ngrok")
        break
    
    elif input1 == "n": 
        data = configparser.ConfigParser(allow_no_value=True)
        data.read("Data/config.ini")
        data.set("Settings", "ngrok", "False")
        with open("Data/config.ini", "w") as configfile: data.write(configfile) #Uložení
        break

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

try: os.mkdir("Modules/ngrok/data")
except: None
input2 = input("Ngrok token: ")
try: file = open("Modules/ngrok/data/ngrok.txt", "a").close()
except: None
file = open("Modules/ngrok/data/ngrok.txt", "w")
file.write(input2)
file.close()

input3 = input("Discord bot token: ")
try: file = open("Modules/ngrok/data/token.txt", "a").close()
except: None
file = open("Modules/ngrok/data/token.txt", "w")
file.write(input3)
file.close()

data = configparser.ConfigParser(allow_no_value=True)
data.read("Data/config.ini")
data.set("Settings", "wiki_finder_online", "True")
with open("Data/config.ini", "w") as configfile: data.write(configfile) #Uložení

print("Instalace dokončena")