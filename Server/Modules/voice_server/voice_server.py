
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
        connected = False
        SERVER_CERTIFICATE = data.read(f"{os.getcwd()}/Data/certificate.ini", "Certificate", "server")
        CLIENT_CERTIFICATE = data.read(f"{os.getcwd()}/Data/certificate.ini", "Certificate", "client")
        #print(f' New client: "{addr[0]}:{addr[1]}" (Active connections: {threading.active_count() - 1})')
        if conn.recv(2048).decode("utf-8") == CLIENT_CERTIFICATE: #Bezpečnostní ověření
            conn.send(SERVER_CERTIFICATE.encode("utf-8"))

            file = open("Client_updater/client-core.py", "r")
            for line in file.readlines(): #Získání verze klienta tady na serveru
                if "VERSION = " in line:
                    client_version = line.replace("VERSION = ", "").replace('"', "").replace("\n", "")
            file.close()
            
            info = conn.recv(2048).decode("utf-8").split(", ")
            user = AuthStore.login(info[1], info[2])
            if user["status"] == "Auth_error": 
                conn.send("Auth_error".encode("utf-8"))
                register = conn.recv(2048).decode("utf-8").replace("Register ", "").split(", ")
                user = AuthStore.register(register[0], register[1])

            if info[0][2:] > client_version[2:]: conn.send("Version_error".encode("utf-8"))
            elif info[0][2:] < client_version[2:]:
                file = open("Client_updater/client-core.py", "r")
                data0 = file.read()
                file.close()
                conn.send(data0.encode("utf-8"))
            else: 
                conn.send("No_new_update".encode("utf-8"))
                connected = True

            while connected: #Zahájení připojení
                try:
                    lenght = int(conn.recv(2048).decode("utf-8")) #Přijme informaci o velikosti dat
                    message = conn.recv(lenght+100).decode("utf-8") #Přijme zprávu o velikosti lenght
                    try: 
                        if message: #Zpracování a odpověd
                            conn.send(Engine.process(user, message).encode("utf-8"))
                    except: None
                except: #Pokud dojde k chybě, nebo se klient odpojí, uzavři spojení
                    #print(f" Client {addr} disconnected (Active connections: {threading.active_count() - 2})")
                    connected = False
            conn.close()
        else: #Pokud se neověří
            print(f" Client {addr} suspicious activity, connection terminated (Active connections: {threading.active_count() - 2})")
            conn.close()