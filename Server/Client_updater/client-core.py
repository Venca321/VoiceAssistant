import socket, threading, time, os, signal, configparser

certificate = configparser.ConfigParser(allow_no_value=True)
certificate.read(f"certificate.ini")

PORT = 25050
host = certificate.get("Host", "automatic")
VERSION = "v.0.0"
SERVER_CERTIFICATE = certificate.get("Certificate", "server")
CLIENT_CERTIFICATE = certificate.get("Certificate", "client")

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

if client.recv(2048).decode("utf-8") == SERVER_CERTIFICATE: #Client auth
    client.send(CLIENT_CERTIFICATE.encode("utf-8"))
    top_version = client.recv(2048).decode("utf-8") #Zjištění server verze
    client.send("Updated".encode("utf-8")) #Autoupdate

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