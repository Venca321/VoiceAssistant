
import sqlite3

DATABASE_FILE = "Data/Database/database.db"

class db():
    def setup_my_db():
        """
        Setupne databázy (přidá vše potřebné do ní)
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try: cursor.execute(f"create table users (username text, email text, password text)")
        except: None
        try: cursor.execute(f"create table user_settings (username text, email text, password text, addressing text, name text, animation_speed integer)")
        except: None
        try: cursor.execute(f"create table log (username text, password text, time text, request text, response text)")
        except: None

        connection.close()

    def setup_user(username:str, email:str, password:str):
        """
        Setupne uživatele (vytvoří defaultní nastavení...)
        """
        db.write("user_settings", (username, email, password, "---", "---", 1))

    def register(username:str, email:str, password:str, repeat_password:str):
        """
        Registruje uživatele
        """
        if not email == "alfa-tester@token.cz": return "Neplatný alfa token"
        if not username or len(username) < 4 or " " in username: return "Neplatné uživatelské jméno"
        if not password or len(password) < 8 or " " in password: return "Neplatné heslo"
        if not password == repeat_password: return "Hesla se neshodují"

        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute(f"select * from users where (username=:username or email=:username) and password=:password", {"username": username, "password": password})
        user = cursor.fetchall()
        if not user: 
            cursor.execute(f"insert into users values (?,?,?)", (username, email, password))
            connection.commit()
            connection.close()

            db.setup_user(username, email, password)

            return True
        else:
            connection.close()
            return "Error"

    def login(username_or_email:str, password:str):
        """
        Checkne přihlášení uživatele
        """
        if not username_or_email: return "Zadejte uživatelské jméno"
        if not password: return "Zadejte heslo"

        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(f"select * from users where (username=:username_or_email or email=:username_or_email) and password=:password", {"username_or_email": username_or_email, "password": password})
            user = cursor.fetchall()
        except: None
        
        connection.close()
        if user: return True
        return "Neplatné uživatelské jméno nebo heslo"

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
        if not "username" in command or not "password" in command or not "username" in parametrs or not "password" in parametrs: return "AuthError"
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(command, parametrs)
            connection.commit()
        except: None
        
        connection.close()
