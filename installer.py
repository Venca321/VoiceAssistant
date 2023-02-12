
import os, random, string, socket

def get_random_string(length): #Generování certifikátu
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

while True:
    input1 = input("Can I install required modules from requirements.txt (Y/n)? ").lower()
    if input1 == "y" or input1 == "": break
    elif input1 == "n": exit()
    
os.system('pip install -r requirements.txt') #Instalace requirements.txt

while True:
    input2 = input("You want to generate certificates (otherwise you have to insert your own) (Y/n)? ").lower()
    if input2 == "y" or input2 == "" or input2 == "n": break

if input2 == "" or input2.lower() == "y":
    server_certificate = get_random_string(64)
    client_certificate = get_random_string(64)

else:
    print('You need to insert two different certificates in the form: "K25hd4lAHslH4Lh3alskdj"')
    server_certificate = input("Your server certificate: ")
    client_certificate = input("Your client certificate: ")

print(f"Your client certificate is: {client_certificate}")
print(f"Your server certificate is: {server_certificate}")

while True:
    input3 = input("You wish to set up these certificates automatically (Y/n)? ").lower()
    if input3 == "y" or input3 == "": break
    elif input3 == "n": exit()

try: os.remove(f"{os.getcwd()}/Client/certificate.ini") #Setup certifikátů
except: None
try: os.remove(f"{os.getcwd()}/Server/Data/certificate.ini")
except:None

file = open(f"{os.getcwd()}/Client/certificate.ini", "a").close()
file = open(f"{os.getcwd()}/Server/Data/certificate.ini", "a").close()
file = open(f"{os.getcwd()}/Client/certificate.ini", "w")
file.write(f"[Certificate]\nserver = {server_certificate}\nclient = {client_certificate}\n\n[Host]\nautomatic = {socket.gethostbyname(socket.gethostname())}")
file.close()
file = open(f"{os.getcwd()}/Server/Data/certificate.ini", "a")
file.write(f"[Certificate]\nserver = {server_certificate}\nclient = {client_certificate}")
file.close()

print("Setup completed")