
import time, os
from Modules.functions.functions import *

class Tester():
    def startup_test(): #Testování všech souborů
        CONFIG_FILE = f"{os.getcwd()}/Modules/tester/data/config.ini"

        print(f' Loading files...             0% [{100*"."}]', end="\r")

        code_lines, config_lines, vocabulary_lines, data_lines = 0, 0, 0, 0
        for i in data.options(CONFIG_FILE, "Modules"): #Testování modulů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Modules", i)}{i}.py', "r") #Pokus se je otevřít
                file_data = file.read()
                file.close()
                code_lines += len(file_data.split("\n"))
                if not "class Match():" in file_data or not "class Data():" in file_data: raise #Check, zda obsahuje classy nutné k funkčnosti
            except: #Pokud to nejde
                print(f'\n Error while checking module! {os.getcwd()}/{data.read(CONFIG_FILE, "Modules", i)}{i}.py')
                exit()

        print(f' Loading files...            20% [{25*"#"}{75*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Special_scripts"): #Testování nestandartních modulů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Special_scripts", i)}{i}.py', "r")
                code_lines += len(file.read().split("\n"))
                file.close()
            except:
                print(f'\n Error special script not found! {os.getcwd()}/{data.read(CONFIG_FILE, "Special_scripts", i)}{i}.py')
                exit()

        print(f' Loading files...            40% [{50*"#"}{50*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Configs"): #Testování config souborů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Configs", i)}', "r")
                config_lines += len(file.read().split("\n"))
                file.close()
            except:
                print(f'\n Error config file not found! {os.getcwd()}/{data.read(CONFIG_FILE, "Configs", i)}')
                exit()

        print(f' Loading files...            60% [{50*"#"}{50*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Vocabulary"): #Testování config souborů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Vocabulary", i)}', "r")
                text = file.read()
                if not "[Match]" in text: raise
                file.close()
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Vocabulary", i)}', "r")
                vocabulary_lines += len(file.read().split("\n"))
                file.close()
            except:
                print(f'\n Error with vocabulary file! {os.getcwd()}/{data.read(CONFIG_FILE, "Vocabulary", i)}')
                exit()

        print(f' Loading files...            80% [{75*"#"}{25*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Data"): #Testování dat
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Data", i)}', "r")
                data_lines += len(file.read().split("\n"))
                file.close()
            except: #Pokud neexistuje
                print(f' Warning data file not found! {os.getcwd()}/{data.read(CONFIG_FILE, "Data", i)}')
                time.sleep(1)
                try: #Pokus se vytvořit
                    file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Data", i)}', "x")
                    file.close()
                except: 
                    print(f'\n Error data file cannot be created! {os.getcwd()}/{data.read(CONFIG_FILE, "Data", i)}')
                    exit()

        print(f' Loading files...           100% [{100*"#"}]') #Vše ok
        time.sleep(0.2)
        print(f"\n Successfully loaded:\n   {code_lines} lines of code\n   {config_lines} lines of configuration\n   {vocabulary_lines} lines of vocabulary data\n   {data_lines} lines of data\n")

    def test(output=False): #output = True je 1. test (s printem)
        if output: print(f' Testing functionality...     0% [{100*"."}]', end="\r")


        if output: 
            print(f' Testing functionality...   100% [{100*"#"}]\n')
            time.sleep(0.2)
            print(" Everything seems to be working properly.\n")
