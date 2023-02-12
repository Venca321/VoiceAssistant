import socket, threading, time, os, signal, configparser

certificate = configparser.ConfigParser(allow_no_value=True)
certificate.read(f"certificate.ini")

PORT = 25050
host = certificate.get("Host", "automatic")
VERSION = "v.0.0"
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
    print("Error automatic host not working")
    host = input("Host: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Client connect
    client.connect((host, PORT))

if client.recv(2048).decode("utf-8") == SERVER_CERTIFICATE: #Client auth
    client.send(CLIENT_CERTIFICATE.encode("utf-8"))
    top_version = client.recv(2048).decode("utf-8") #Zjištění server verze
    if float(top_version[2:]) > float(VERSION[2:]):
        client.send("Need_update_pls".encode("utf-8")) #Autoupdate
        input1 = input("\n New version available, please confirm update [Y/n] ")
        if input1.lower() == "y" or input1.lower() == "":
            print(" Updating...")
            data = client.recv(48152).decode("utf-8")
            file = open("new_client.py", "a")
            file.close()
            file = open("new_client.py", "w")
            file.write(data)
            file.close()
            os.system("python clientautoupdate.py")
            client.close()
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

print(f"\n Successfully connected with version {VERSION}\n")

def send(msg): #Send fce
    msg_lengh = str(len(msg))
    client.send((msg_lengh.encode("utf-8")))
    time.sleep(0.05)
    client.send((msg.encode("utf-8")))

def my_recv(): #Recv část
    while True:
        message = client.recv(2048).decode("utf-8")
        if message: print(f"{message}")

def my_sender(): #Sender část
    while True:
        text = input("")
        if text: send(text)

threading.Thread(target=my_sender).start()
threading.Thread(target=my_recv).start()