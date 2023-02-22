
from Modules.functions.functions import *
import os

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
            if Userdata.decode(data.read(f"{os.getcwd()}/Data/users.ini", "Users", i), password) == password and Userdata.decode(i, password) == username:
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
        data.write(f"{os.getcwd()}/Data/users.ini", "Users", Userdata.encode(username, password), Userdata.encode(password, password))
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
