
from Modules.functions.functions import *
import os

class AuthStore():
    """
    AuthStore.username vrátí uživatelské jméno, kterým je uživatel přihlášen
    AuthStore.password vrátí heslo, kterým je uživatel přihlášen
    """
    def login(username:str, password:str, second_try:bool=False):
        """
        Přihlásit uživatele
        """
        for i in data.options(f"{os.getcwd()}/Data/users.ini", "Users"):
            if Userdata.decode(data.read(f"{os.getcwd()}/Data/users.ini", "Users", i), password) == password and Userdata.decode(i, password) == username:
                user = {}
                user["username"] = username
                user["password"] = password
                return user
        
        return AuthStore.register(username, password)

    def register(username:str, password:str):
        """
        Registruje uživatele
        """
        data.write(f"{os.getcwd()}/Data/users.ini", "Users", Userdata.encode(username, password), Userdata.encode(password, password))
        UserData.check_files()
        return AuthStore.login(username, password, True)

class UserData():
    def check_files():
        """
        Zkontroluje, že .userdata/uživatelské_jméno exituje všude, kde má
        """
        if AuthStore.username and not AuthStore.username == "Tester(6982734987923668712639127318923)!!!":
            data_locations = data.options(f"{os.getcwd()}/Modules/tester/data/config.ini", "User_data")
            for location in data_locations:
                location = data.read(f"{os.getcwd()}/Modules/tester/data/config.ini", "User_data", location)
                try:
                    file = open(f'{location}.userdata/{AuthStore.username}.ini', "x")
                    file.close()
                except: None
