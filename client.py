import socket, threading, time, glob

LOCATION = "MIA\\"
PORT = 25050
HOST = "192.168.0.10"
SERVER_CERTIFIKATE = "alsjdhaksjdamcxnjahkjdshkjgfajhsflhdkjsahjkfdhasjkfhaskjfhxbacnxbahjsgdkabskfjhkauheuhrwhukawhaslashfjashkjfhasgdjhasgfjhagsfjhgashfgjgafjhgsajhfguzawroawushdkabcsmbvahsgfdjgweqiurz"
CLIENT_CERTIFIKATE = "hjkahsdkjabnsckjalwdLHJAFJSNflsAHFlhfalsHfljashfljhadslNFBjhsLKFHsalfhhflASHJlfhASJLDhfljashfljashlfhlsAHfljahsfjhaLJSFhLAJHlhFSlajhfaljhfLhLJhLFajshaljshfLJHFLFshlsfahlJASHflshljsa"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
if client.recv(2048).decode("utf-8") == SERVER_CERTIFIKATE: client.send(CLIENT_CERTIFIKATE.encode("utf-8"))
else: 
    client.close()
    exit()

print("\n")

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
        time.sleep(0.1)
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