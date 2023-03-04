
from Modules.functions.functions import *
from cryptography.fernet import Fernet
import base64, os

class AuthStore():
    """
    AuthStore.username vrátí uživatelské jméno, kterým je uživatel přihlášen
    AuthStore.password vrátí heslo, kterým je uživatel přihlášen
    """
    def login(username:str, password:str):
        """
        Přihlásit uživatele
        """
        for i in data.options(f"{os.getcwd()}/Data/users.ini", "Users"):
            y = data.read(f"{os.getcwd()}/Data/users.ini", "Users", i).split("**/**")
            if UserData.decode(y[0], password) == username and UserData.decode(y[1], password) == password:
                user = {}
                user["status"] = "ok"
                user["username"] = username
                user["password"] = password
                return user
        
        user = {}
        user["status"] = "Auth_error"
        return user

    def register(username:str, password:str):
        """
        Registruje uživatele
        """
        num = 0
        finished = False
        while not finished: #Získá 1. dostupné číslo v sekci [Notes]
            if not str(num) in data.options(f"{os.getcwd()}/Data/users.ini", "Users"):
                option = num
                finished = True
            else: num += 1
        data.write(f"{os.getcwd()}/Data/users.ini", "Users", str(option), f'{UserData.encode(username, password)}**/**{UserData.encode(password, password)}') #Zapíše data
        
        UserData.check_files(username)

        user = {}
        user["status"] = "ok"
        user["username"] = username
        user["password"] = password
        return user

class UserData():
    def check_files(username:str):
        """
        Zkontroluje, že .userdata/uživatelské_jméno exituje všude, kde má
        """
        if username and not username == "Tester(6982734988923)":
            data_locations = data.options(f"{os.getcwd()}/Modules/tester/data/config.ini", "User_data")
            for location in data_locations:
                location = data.read(f"{os.getcwd()}/Modules/tester/data/config.ini", "User_data", location)
                try:
                    file = open(f'{location}.userdata/{username}.ini', "x")
                    file.close()
                except: None

    def encode(text:str, password:str):
        """
        Vrátí text zakódovaný heslem 
        """
        key = base64.b64encode(f"{password:<32}".encode("utf-8"))
        encryptor = Fernet(key=key)
        return (encryptor.encrypt(text.encode("utf-8")).decode("utf-8")).replace("=", ".,.")

    def decode(encrypted:str, password:str):
        """
        Vrátí text rozkódovaný heslem
        """
        try:
            key = base64.b64encode(f"{password:<32}".encode("utf-8"))
            encryptor = Fernet(key=key)
            return encryptor.decrypt(encrypted.replace(".,.", "=").encode("utf-8")).decode("utf-8")
        except: return
