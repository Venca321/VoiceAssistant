
from Modules.functions.functions import *
import os

class AuthStore():
    """
    AuthStore.username vrátí uživatelské jméno, kterým je uživatel přihlášen
    AuthStore.password vrátí heslo, kterým je uživatel přihlášen
    """
    def login(self, username:str, password:str):
        """
        Přihlásit uživatele
        """
        self.username = username
        self.password = password
        UserData.check_files()

    def logout(self):
        """
        Odhlásit uživatele - není nutné (po zaniknutí připojení se odhlásí samo)
        """
        self.username = None
        self.password = None

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
