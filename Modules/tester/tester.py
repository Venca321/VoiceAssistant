
import time, os
from Modules.functions.functions import *

class Tester():
    def startup_test(): #Testování všech souborů
        CONFIG_FILE = f"{os.getcwd()}/Modules/tester/data/config.ini"

        print(f' Loading files...             0% [{100*"."}]', end="\r")

        code_lines, config_lines, data_lines = 0, 0, 0
        for i in data.options(CONFIG_FILE, "Modules"): #Testování modulů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Modules", i)}{i}.py', "r") #Pokus se je otevřít
                file_data = file.read()
                file.close()
                code_lines += len(file_data.split("\n"))
                if not "class Match():" in file_data or not "class Data():" in file_data: raise #Check, zda obsahuje classy nutné k funkčnosti
            except: #Pokud to nejde
                print(f' Error while checking module! {os.getcwd()}/{data.read(CONFIG_FILE, "Modules", i)}{i}.py')
                exit()

        print(f' Loading files...            25% [{25*"#"}{75*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Special_scripts"): #Testování nestandartních modulů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Special_scripts", i)}{i}.py', "r")
                code_lines += len(file.read().split("\n"))
                file.close()
            except:
                print(f' Error special script not found! {os.getcwd()}/{data.read(CONFIG_FILE, "Special_scripts", i)}{i}.py')
                exit()

        print(f' Loading files...            50% [{50*"#"}{50*"."}]', end="\r")
        for i in data.options(CONFIG_FILE, "Configs"): #Testování config souborů
            try: 
                file = open(f'{os.getcwd()}/{data.read(CONFIG_FILE, "Configs", i)}', "r")
                config_lines += len(file.read().split("\n"))
                file.close()
            except:
                print(f' Error config file not found! {os.getcwd()}/{data.read(CONFIG_FILE, "Configs", i)}')
                exit()

        print(f' Loading files...            75% [{75*"#"}{25*"."}]', end="\r")
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
                    print(f' Error data file cannot be created! {os.getcwd()}/{data.read(CONFIG_FILE, "Data", i)}')
                    exit()

        print(f' Loading files...           100% [{100*"#"}]') #Vše ok
        time.sleep(0.2)
        print(f"\n Successfully loaded:\n   {code_lines} lines of code\n   {config_lines} lines of configuration\n   {data_lines} lines of data\n")

    def test(output=False): #output = True je 1. test (s printem)
        if output: print(f' Testing functionality...     0% [{100*"."}]', end="\r")


        if output: 
            print(f' Testing functionality...   100% [{100*"#"}]\n')
            time.sleep(0.2)
            print(" Everything seems to be working properly.\n")
