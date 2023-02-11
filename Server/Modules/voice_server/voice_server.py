
from Modules.functions.functions import *
from Modules.engine.engine import *
import socket, threading, os

class Voice_server():
    def start():
        PORT = int(data.read(f"{os.getcwd()}/Modules/voice_server/data/config.ini", "Settings", "port"))
        HOST = socket.gethostbyname(socket.gethostname()) #IP počítače

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Vytvoření serveru
            server.bind((HOST, PORT))
        except:
            print(" Comunication error, cannot bind address!")
            os._exit(1)

        server.listen()
        #print(f" Server online ({HOST}:{PORT})\n") ##################
        while True: #Pro každé zařízení vlastní thread (každé se spracovává zvlášť)
            conn, addr = server.accept()
            thread = threading.Thread(target=Voice_server.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(conn, addr): #Handle jednotlivých klientů
        SERVER_CERTIFIKATE = data.read(f"{os.getcwd()}/Data/certifikate.ini", "Certifikate", "server")
        CLIENT_CERTIFIKATE = data.read(f"{os.getcwd()}/Data/certifikate.ini", "Certifikate", "client")
        #print(f' New client: "{addr[0]}:{addr[1]}" (Active connections: {threading.active_count() - 1})')
        conn.send(SERVER_CERTIFIKATE.encode("utf-8")) #Bezpečnostní ověření
        if conn.recv(2048).decode("utf-8") == CLIENT_CERTIFIKATE: #Pokud se ověří

            file = open("client.py", "r")
            client_version = file.readlines()[4].replace("\n", "").replace('"', "").replace("VERSION = ", "") #Získání verze klienta tady na serveru
            file.close()
            conn.send(client_version.encode("utf-8")) #Poslání verze klienta
            need_update = conn.recv(2048).decode("utf-8") 

            if need_update == "Need_update_pls": #Pokud potřebuje update:
                file = open("client.py", "r", encoding="utf-8") #Přeposlání souboru
                data0 = file.read()
                file.close()
                conn.send(data0.encode("utf-8")) #...
                
            connected = True 
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