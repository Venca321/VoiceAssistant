
import os

try:
    import socket, threading, time, os, signal, configparser
except:
    while True:
        input1 = input("Problém s importováním knihoven, mohu je nainstalovat (Y/n)? ").lower()
        if input1 == "n": exit()
        elif input == "y" or input1 == "": break
    os.system("pip install -r requirements.txt")

certificate = configparser.ConfigParser(allow_no_value=True)
certificate.read(f"certificate.ini")

PORT = 25050
host = certificate.get("Host", "automatic")
VERSION = certificate.get("Client", "version")
SERVER_CERTIFICATE = certificate.get("Certificate", "server")
CLIENT_CERTIFICATE = certificate.get("Certificate", "client")

def handle_exit(signum, frame):
    client.close()
    os._exit(1)

signal.signal(signal.SIGINT, handler=handle_exit)

os.system("clear")

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Client connect
    client.connect((host, PORT))
except:
    print("Nelze se automaticky připojit k hostiteli")
    host = input("Host: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Client connect
    client.connect((host, PORT))

if client.recv(2048).decode("utf-8") == SERVER_CERTIFICATE: #Client auth
    client.send(CLIENT_CERTIFICATE.encode("utf-8"))
    top_version = client.recv(2048).decode("utf-8") #Zjištění server verze
    if VERSION[2:] == "?.?":
        client.send("Updated".encode("utf-8"))
        client.close()
        os.system("python client-core.py")
        os._exit(1)
    if float(top_version[2:]) > float(VERSION[2:]):
        client.send("Need_update_pls".encode("utf-8")) #Autoupdate
        input1 = input("\n Je dostupná nová verze, prosím potvrďte aktualizaci [Y/n] ")
        if input1.lower() == "y" or input1.lower() == "":
            print(" Aktualizování...")
            data = client.recv(48152).decode("utf-8")
            file = open("client-core.py", "w")
            file.write(data)
            file.close()
            client.close()
            os.system("python client-core.py")
            os._exit(1)

    elif float(top_version[2:]) == float(VERSION[2:]):
        client.send("Updated".encode("utf-8"))
        client.close()
        os.system("python client-core.py")
        os._exit(1)

    elif float(top_version[2:]) < float(VERSION[2:]): #Pokud je tady větší verze než na serveru, error
        print(" Version Error")
        client.close()
        os._exit(1)
    else: client.send("Updated".encode("utf-8"))
else: 
    print(" Auth Error") #Auth error
    client.close()
    os._exit(1)