
import time, os, socket, csv
from Modules.functions.functions import *

class Tester():
    def startup_test(): #Testování všech souborů
        """
        Zkontroluje přítomnost všech modulů a dalších souborů /data/config.ini
        """
        CONFIG_FILE = f"{os.getcwd()}/Modules/tester/data/config.ini"

        print(f' Loading files...             0% [{100*"."}]', end="\r")

        code_lines, config_lines, vocabulary_lines, wiki_data = 0, 0, 0, 0
        for i in data.options(CONFIG_FILE, "Modules"): #Testování modulů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Modules", i)}{i}.py', "r") #Pokus se je otevřít
                file_data = file.read()
                file.close()
                code_lines += len(file_data.split("\n"))
                if not "class Match():" in file_data or not "class Data():" in file_data: raise #Check, zda obsahuje classy nutné k funkčnosti
            except: #Pokud to nejde
                print(f'\n Error while checking module! {os.getcwd()}/{data.read(CONFIG_FILE, "Modules", i)}{i}.py')
                os._exit(1)

        print(f' Loading files...            20% [{20*"#"}{80*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Special_scripts"): #Testování nestandartních modulů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Special_scripts", i)}{i}.py', "r")
                code_lines += len(file.read().split("\n"))
                file.close()
            except:
                print(f'\n Error special script not found! {os.getcwd()}/{data.read(CONFIG_FILE, "Special_scripts", i)}{i}.py')
                os._exit(1)

        print(f' Loading files...            40% [{40*"#"}{60*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Configs"): #Testování config souborů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Configs", i)}', "r")
                config_lines += len(file.read().split("\n"))
                file.close()
            except:
                print(f'\n Error config file not found! {os.getcwd()}/{data.read(CONFIG_FILE, "Configs", i)}')
                os._exit(1)

        print(f' Loading files...            60% [{60*"#"}{40*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Vocabulary"): #Testování config souborů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Vocabulary", i)}', "r")
                text = file.read()
                file.close()
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Vocabulary", i)}', "r")
                vocabulary_lines += len(file.read().split("\n"))
                file.close()
            except:
                print(f'\n Error with vocabulary file! {os.getcwd()}/{data.read(CONFIG_FILE, "Vocabulary", i)}')
                os._exit(1)

        print(f' Loading files...            80% [{80*"#"}{20*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Other_data"): #Testování dat
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Other_data", i)}', "r")
                file.close()
            except: #Pokud neexistuje
                print(f'\n Warning data file not found! {os.getcwd()}/{data.read(CONFIG_FILE, "Other_data", i)}')
                time.sleep(1)
                try: #Pokus se vytvořit
                    file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Other_data", i)}', "x")
                    file.close()
                except: 
                    print(f'\n Error data file cannot be created! {os.getcwd()}/{data.read(CONFIG_FILE, "Other_data", i)}')
                    os._exit(1)

        for i in data.options(CONFIG_FILE, "User_data"): #Testování dat
            i_path = data.read(CONFIG_FILE, "User_data", i)
            try: 
                path = os.path.join(os.getcwd(), i_path, ".userdata/")
                os.mkdir(path)
            except: None

        WEB_WIKI = data.read(f"{os.getcwd()}/Data/config.ini", "Settings", "wiki_finder_online")
        if WEB_WIKI == "False":
            wikidata = csv.reader(open(f"{os.getcwd()}/Data/wikidata/wikidata.csv", "r"))
            for row in wikidata: wiki_data += 1

        print(f' Loading files...           100% [{100*"#"}]') #Vše ok
        time.sleep(0.2)
        print(f"\n Successfully loaded ({code_lines+config_lines+vocabulary_lines} lines):\n   {code_lines} lines of code\n   {config_lines} lines of configuration\n   {vocabulary_lines} lines of vocabulary data\n   {wiki_data} wikidata pages\n")

    def test(output:bool=False): #output = True je 1. test (s printem)
        """
        Otestuje funkčnost server systému
        """
        if output: print(f' Testing functionality...     0% [{100*"."}]', end="\r")

        SERVER_CERTIFICATE = data.read(f"{os.getcwd()}/Data/certificate.ini", "Certificate", "server")
        CLIENT_CERTIFICATE = data.read(f"{os.getcwd()}/Data/certificate.ini", "Certificate", "client")
        PORT = int(data.read(f"{os.getcwd()}/Modules/voice_server/data/config.ini", "Settings", "port"))
        HOST = socket.gethostbyname(socket.gethostname())

        file = open("Client_updater/client-core.py", "r")
        for line in file.readlines(): #Získání verze klienta tady na serveru
            if "VERSION = " in line:
                client_version = line.replace("VERSION = ", "").replace('"', "").replace("\n", "")
        file.close()

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Client connect
            client.connect((HOST, PORT))
            if output: print(f' Testing functionality...    20% [{20*"#"}{80*"."}]', end="\r")
        except:
            print("\n [Testing] Error connectiong to host...")
            client.close()
            return

        try:
            client.send(CLIENT_CERTIFICATE.encode("utf-8"))
            if client.recv(2048).decode("utf-8") == SERVER_CERTIFICATE: #Client auth
                if output: print(f' Testing functionality...    40% [{40*"#"}{60*"."}]', end="\r")
        except:
            print("\n [Testing] Auth error...")
            client.close()
            return

        try:
            client.send(f"{client_version}, Tester(6982734988923), 9823649269".encode("utf-8"))
            out = client.recv(2048).decode("utf-8") #Zjištění server verze
            if out == "Auth_error":
                client.send(f"Register Tester(6982734988923), 9823649269".encode("utf-8"))
                client.recv(2048).decode("utf-8") #Zjištění server verze
            if output: print(f' Testing functionality...    60% [{60*"#"}{40*"."}]', end="\r")
        except:
            print("\n [Testing] Version error...")
            client.close()
            return

        try:
            client.send((str(len("9H9k2bm!&64iNoerHuwB@HkON")).encode("utf-8")))
            time.sleep(0.1)
            client.send("9H9k2bm!&64iNoerHuwB@HkON".encode("utf-8"))
            out = client.recv(2048).decode("utf-8")
            if not out == "nNq8j3ma15G^KXaV33Ma*W^Rj": raise
            if output: print(f' Testing functionality...    80% [{80*"#"}{20*"."}]', end="\r")
        except:
            print("\n [Testing] Comunication error...")
            client.close()
            return

        client.close()
        if output: 
            print(f' Testing functionality...   100% [{100*"#"}]')
            time.sleep(0.2)
            print(f" Everything seems to be working properly (Server on: {HOST})\n")
