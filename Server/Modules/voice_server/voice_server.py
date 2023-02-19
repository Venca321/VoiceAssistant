
from Modules.functions.functions import *
from Modules.engine.engine import *
from Modules.user_manager.user_manager import AuthStore
import socket, threading, os, time

class Voice_server():
    def start():
        """
        Startne voice server systém
        """
        PORT = int(data.read(f"{os.getcwd()}/Modules/voice_server/data/config.ini", "Settings", "port"))
        HOST = socket.gethostbyname(socket.gethostname()) #IP počítače

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Vytvoření serveru
            server.bind((HOST, PORT))
        except:
            print(" Comunication error, cannot bind address! Please wait before trying again.")
            os._exit(1)

        server.listen()
        #print(f" Server online ({HOST}:{PORT})\n") ##################
        while True: #Pro každé zařízení vlastní thread (každé se spracovává zvlášť)
            conn, addr = server.accept()
            thread = threading.Thread(target=Voice_server.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(conn, addr): #Handle jednotlivých klientů
        """
        Handle pro jednotlivé klienty
        """
        SERVER_CERTIFICATE = data.read(f"{os.getcwd()}/Data/certificate.ini", "Certificate", "server")
        CLIENT_CERTIFICATE = data.read(f"{os.getcwd()}/Data/certificate.ini", "Certificate", "client")
        #print(f' New client: "{addr[0]}:{addr[1]}" (Active connections: {threading.active_count() - 1})')
        conn.send(SERVER_CERTIFICATE.encode("utf-8")) #Bezpečnostní ověření
        if conn.recv(2048).decode("utf-8") == CLIENT_CERTIFICATE: #Pokud se ověří

            file = open("Client_updater/client-core.py", "r")
            for line in file.readlines(): #Získání verze klienta tady na serveru
                if "VERSION = " in line:
                    client_version = line.replace("VERSION = ", "").replace('"', "").replace("\n", "")
            file.close()
            conn.send(client_version.encode("utf-8")) #Poslání verze klienta
            need_update = conn.recv(2048).decode("utf-8") 

            if need_update == "Need_update_pls": #Pokud potřebuje update:
                file = open("Client_updater/client-core.py", "r")
                data0 = file.read()
                file.close()
                conn.send(data0.encode("utf-8")) #...

            try:
                conn.send("!Send-Username?".encode("utf-8"))
                username = conn.recv(2048).decode("utf-8")
                conn.send("!Send-Password?".encode("utf-8"))
                password = conn.recv(2048).decode("utf-8")
                AuthStore.login(AuthStore, username, password)
            except: None
                
            if not AuthStore.username == "" or AuthStore.password == "": connected = True 
            else: connected = False
            while connected: #Zahájení připojení
                try:
                    lenght = int(conn.recv(2048).decode("utf-8")) #Přijme informaci o velikosti dat
                    message = conn.recv(lenght+100).decode("utf-8") #Přijme zprávu o velikosti lenght
                    try: 
                        if message: #Zpracování a odpověd
                            conn.send(Engine.process(message).encode("utf-8"))
                    except: None
                except: #Pokud dojde k chybě, nebo se klient odpojí, uzavři spojení
                    #print(f" Client {addr} disconnected (Active connections: {threading.active_count() - 2})")
                    connected = False
            conn.close()
        else: #Pokud se neověří
            print(f" Client {addr} suspicious activity, connection terminated (Active connections: {threading.active_count() - 2})")
            conn.close()