
import sqlite3

DATABASE_FILE = "Data/database.db"

class db():
    def setup_my_db():
        """
        Setupne databázy (přidá vše potřebné do ní)
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try: cursor.execute(f"create table users (username text, email text, password text)")
        except: None
        try: cursor.execute(f"create table log (username text, password text, time text, request text, response text)")
        except: None

        connection.close()

    def register(username:str, email:str, password:str):
        """
        Registruje uživatele
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute(f"select * from users where (username=:username or email=:username) and password=:password", {"username": username, "password": password})
        user = cursor.fetchall()
        if not user: 
            cursor.execute(f"insert into users values (?,?,?)", (username, email, password))
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return False

    def login(username_or_email:str, password:str):
        """
        Checkne přihlášení uživatele
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(f"select * from users where (username=:username_or_email or email=:username_or_email) and password=:password", {"username_or_email": username_or_email, "password": password})
            user = cursor.fetchall()
        except: None
        
        connection.close()
        if user: return True
        return False

    def write(table:str, items:tuple):
        """
        Vloží jeden řádek to kolekce
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(f"insert into {table} values ({(len(items) * '?,')[:-1]})", items)
            connection.commit()
        except: None

        connection.close()

    def write_multiple(table:str, items:list):
        """
        Vloží více řádků do kolekce
        items = [(neco, neco2), (neco, neco2)]
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try:
            cursor.executemany(f"insert into {table} values ({(len(items[0]) * '?,')[:-1]})", items)
            connection.commit()
        except: None

        connection.close()

    def read(user:dict, table:str):
        """
        returne hodnoty s daným filtrem
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(f"select * from {table} where username=:username and password=:password", {"username": user["username"], "password": user["password"]})
            data = cursor.fetchall()
        except: None

        connection.close()

        return data
    
    def command(command:str, parametrs:dict):
        """
        Provede specifický příkaz --security risk
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(command, parametrs)
            connection.commit()
        except: None
        
        connection.close()
