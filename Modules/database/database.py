
import sqlite3, random, string

DATABASE_FILE = "Data/Database/database.db"

def get_id(length):
    while True:
        new_id = "".join(random.choice(string.ascii_letters+string.digits) for i in range(length))
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()
        cursor.execute(f"select * from users where id=:id", {"id": new_id})
        if cursor.fetchall(): connection.close()
        else: break
    return new_id

class db():
    def setup_my_db():
        """
        Setupne databázy (přidá vše potřebné do ní)
        """
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try: cursor.execute(f"create table users (id text, username text, email text, password text)")
        except: None
        try: cursor.execute(f"create table user_settings (id text, addressing text, name text, animation_speed integer)")
        except: None
        try: cursor.execute(f"create table log (id text, time text, request text, response text)")
        except: None

        connection.close()

    def setup_user(user:dict):
        """
        Setupne uživatele (vytvoří defaultní nastavení...)
        """
        db.write("user_settings", (user["id"], "---", "---", 1))

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

        cursor.execute(f"select * from users where username=:username", {"username": username})
        if cursor.fetchall(): 
            connection.close()
            return "Uživatelské jméno již existuje"
        
        """
        cursor.execute(f"select * from users where email=:email", {"email":email})
        if cursor.fetchall():
            connection.close()
            return "E-mail je již zaregistrován" 
        """

        id = get_id(25)
        cursor.execute(f"insert into users values (?,?,?,?)", (id, username, email, password))
        connection.commit()
        connection.close()

        user = {
            "id": id,
            "username": username,
            "password": password
        }
        db.setup_user(user)

        return user

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
        if user: 
            user = {
                "id": user[0][0],
                "username": user[0][1],
                "password": user[0][3]
            }

            return user
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
            cursor.execute(f"select * from {table} where id=:id", {"id": user["id"]})
            data = cursor.fetchall()
        except: None

        connection.close()

        return data
    
    def command(command:str, parametrs:dict):
        """
        Provede specifický příkaz --security risk
        """
        if not "id" in command or not "id" in parametrs: return "AuthError"
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute(command, parametrs)
            connection.commit()
        except: None
        
        connection.close()
