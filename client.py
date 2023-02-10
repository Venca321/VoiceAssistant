import socket, threading, time, glob, os, signal

LOCATION = "MIA\\"
PORT = 25050
HOST = "192.168.0.10"
VERSION = "v.0.0"
SERVER_CERTIFIKATE = "alsjdhaksjdamcxnjahkjdshkjgfajhsflhdkjsahjkfdhasjkfhaskjfhxbacnxbahjsgdkabskfjhkauheuhrwhukawhaslashfjashkjfhasgdjhasgfjhagsfjhgashfgjgafjhgsajhfguzawroawushdkabcsmbvahsgfdjgweqiurz"
CLIENT_CERTIFIKATE = "hjkahsdkjabnsckjalwdLHJAFJSNflsAHFlhfalsHfljashfljhadslNFBjhsLKFHsalfhhflASHJlfhASJLDhfljashfljashlfhlsAHfljahsfjhaLJSFhLAJHlhFSlajhfaljhfLhLJhLFajshaljshfLJHFLFshlsfahlJASHflshljsa"

def handle_exit(signum, frame):
    client.close()
    os._exit(1)

signal.signal(signal.SIGINT, handler=handle_exit)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
if client.recv(2048).decode("utf-8") == SERVER_CERTIFIKATE: 
    client.send(CLIENT_CERTIFIKATE.encode("utf-8"))
    top_version = client.recv(2048).decode("utf-8")
    if float(top_version[2:]) > float(VERSION[2:]): 
        client.send("Need_update_pls".encode("utf-8"))
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
            exit()

    elif float(top_version[2:]) < float(VERSION[2:]):
        print(" Version Error")
        client.close()
        exit()

    else:
        client.send("Updated".encode("utf-8"))
else: 
    print(" Auth Error")
    client.close()
    exit()

print(f"\n Running best version ({VERSION})\n")

def send(msg):
    msg_lengh = str(len(msg))
    client.send((msg_lengh.encode("utf-8")))
    time.sleep(0.1)
    client.send((msg.encode("utf-8")))

def my_recv():
    while True:
        message = client.recv(2048).decode("utf-8")
        if message:
            print("\n", message, "\n")

print(" 1) send file\n 2) Type something \n")

def my_sender():
    while True:
        time.sleep(0.25)
        text = input("--> ")

        if text.lower() == "1":
            name = input("Soubor: ")

            if name.lower() == "all":
                for i in glob.glob(f"{LOCATION}**\*.*", recursive=True):
                    if not "__pycache__" in i:
                        print(i)
                        file = open(i, "r", encoding="utf-8")
                        data = file.read()
                        file.close()
                        send(f'V1 /%/ {i} /%/ {data}')
                        time.sleep(0.1)

            else:
                file = open(LOCATION+name, "r", encoding="utf-8")
                data = file.read()
                file.close()
                send(f"V1 /%/ {LOCATION+name} /%/ {data}")

        else:
            send(text)

threading.Thread(target=my_sender).start()
threading.Thread(target=my_recv).start()