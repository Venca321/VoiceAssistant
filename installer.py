
import os, random, string, socket

def get_random_string(length): #Generování certifikátu
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

while True:
    input1 = input("Mohu instalovat potřebné knihovny z requirements.txt (Y/n)? ").lower()
    if input1 == "y" or input1 == "": break
    elif input1 == "n": exit()
    
os.system('pip install -r requirements.txt') #Instalace requirements.txt

import configparser

while True:
    input2 = input("Chcete automaticky vygenerovat certifikáty (jinak je budete muset manuálně vložit) (Y/n)? ").lower()
    if input2 == "y" or input2 == "" or input2 == "n": break

if input2 == "" or input2.lower() == "y":
    server_certificate = get_random_string(64)
    client_certificate = get_random_string(64)

else:
    print('Musíte vložit dva rozdílné certifikáty typu (doporučuji 50 a více znaků): "K25hd4lAHslH4Lh3alskdj"')
    server_certificate = input("Váš server certifikát: ")
    client_certificate = input("Váš klient certifikát: ")

print(f"Váš klient certifikát je: {client_certificate}")
print(f"Váš server certifikát je: {server_certificate}")

while True:
    input3 = input("Přejete se tyto certifikáty nastavit automaticky (Y/n)? ").lower()
    if input3 == "y" or input3 == "": break
    elif input3 == "n": exit()

try: os.remove(f"{os.getcwd()}/Client/certificate.ini") #Setup certifikátů
except: None
try: os.remove(f"{os.getcwd()}/Server/Data/certificate.ini")
except:None

file = open(f"{os.getcwd()}/Client/certificate.ini", "a").close()
file = open(f"{os.getcwd()}/Server/Data/certificate.ini", "a").close()
file = open(f"{os.getcwd()}/Client/certificate.ini", "w")
file.write(f"[Certificate]\nserver = {server_certificate}\nclient = {client_certificate}\n\n[Host]\nautomatic = {socket.gethostbyname(socket.gethostname())}")
file.close()
file = open(f"{os.getcwd()}/Server/Data/certificate.ini", "a")
file.write(f"[Certificate]\nserver = {server_certificate}\nclient = {client_certificate}")
file.close()

while True:
    input4 = input("Chcete použít vyhledávání informací online (Y/n)?").lower()
    if input4 == "y" or input4 == "": break
    elif input4 == "n": 
        data = configparser.ConfigParser(allow_no_value=True)
        data.read("Server/Data/config.ini")
        data.set("Settings", "wiki_finder_online", "False")
        with open("Server/Data/config.ini", "w") as configfile: file.write(configfile) #Uložení
        print("Než budete pokračovat, postupujte podle dokumentace a stáhněte si wikidata")
        exit()

data = configparser.ConfigParser(allow_no_value=True)
data.read("Server/Data/config.ini")
data.set("Settings", "wiki_finder_online", "True")
with open("Server/Data/config.ini", "w") as configfile: file.write(configfile) #Uložení

print("Instalace dokončena")