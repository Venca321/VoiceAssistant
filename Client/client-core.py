import socket, threading, time, os, signal, configparser

certificate = configparser.ConfigParser(allow_no_value=True)
certificate.read(f"certificate.ini")

PORT = 25050
host = certificate.get("Host", "automatic")
VERSION = "v.0.1"
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

if not certificate.get("Client", "version") == VERSION: 
    certificate.set("Client", "version", VERSION)
    with open("certificate.ini", "w") as configfile: certificate.write(configfile) #Uložení

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

print(f"\n Úspěšně připojeno s verzí {VERSION}\n")

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