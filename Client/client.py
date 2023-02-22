
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

client_username = certificate.get("Client", "username")
client_password = certificate.get("Client", "password")
if client_username == "" or client_password == "":
    print("Nemáte uložené přihlašovací údaje, prosím přihlašte se:")
    client_username = input("Uživatelské jméno: ")
    client_password = input("Heslo: ")
    while True:
        input1 = input("Chcete uložit přihlašovací údaje [Y/n]?").lower()
        if input1 == "n": break
        elif input1 == "y" or input1 == "":
            certificate.set("Client", "username", client_username)
            certificate.set("Client", "password", client_password)
            with open("certificate.ini", "w") as configfile: certificate.write(configfile) #Uložení
            break

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

client.send(CLIENT_CERTIFICATE.encode("utf-8"))
if client.recv(2048).decode("utf-8") == SERVER_CERTIFICATE: #Client auth
    client.send(f"{VERSION}, {client_username}, {client_password}".encode("utf-8"))
    data = client.recv(48152).decode("utf-8")

    if data == "Auth_error":
        client.send(f"Register {client_username}, {client_password}".encode("utf-8"))
        data = client.recv(48152).decode("utf-8")

    if data == "Version_error":
        print(" Version Error")
        client.close()
        os._exit(1)
    
    elif data == "No_new_update":
        client.close()
        os.system("python client-core.py")
        os._exit(1)

    else:
        input1 = input("\n Je dostupná nová verze, prosím potvrďte aktualizaci [Y/n] ")
        if input1.lower() == "y" or input1.lower() == "":
            print(" Aktualizování...")
            file = open("client-core.py", "w")
            file.write(data)
            file.close()
            client.close()
            os.system("python client-core.py")
            os._exit(1)
else: 
    print(" Auth Error") #Auth error
    client.close()
    os._exit(1)