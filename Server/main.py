""" MIA hlasová asistentka (následovník hlasového asistenta trixe) 9. 11. 2022"""

from Modules.tester import tester
from Modules.functions.functions import *
from Modules.voice_server.voice_server import *
from importlib.machinery import SourceFileLoader
import multiprocessing, time, signal, os, subprocess

os.system("clear")
VERSION = data.read(f"{os.getcwd()}/Data/config.ini", "Settings", "version")
MODULES = data.options(f"{os.getcwd()}/Modules/tester/data/config.ini", "Modules")
imported = {}

for x in MODULES: #Automatický import z /Modules/tester/data/config.ini
    try: imported[x] = SourceFileLoader(x,f'{os.getcwd()}/{data.read(f"{os.getcwd()}/Modules/tester/data/config.ini", "Modules", x)}{x}.py').load_module()
    except: print(f" Error importing {x}")

class Threads():
    def autoupdate():
        while True:
            print(" Server updating...")
            subprocess.run(["git", "pull"], capture_output=True) #Auto pull z githubu
            print(" Server updated.\n")
            time.sleep(60*60) #Haždou hodinu

    def tests(): #Automatické testy funkčnosti (updaty souborů, servery...)
        print(" Testing functionality...", end="\r")
        time.sleep(3)
        tester.Tester.test(True)
        time.sleep(60)
        while True:
            start = time.time()
            tester.Tester.test()
            time.sleep(60 - (time.time() - start))

    def data_update(): #V každém souboru Data.update() -- zastupuje data i time_core
        time.sleep(1)
        timer = 0
        while True:
            start = time.time() #start čas
            for i in list(imported.items()): i[1].Data.update(timer) #v každém modulu v Modules Data.update()
            try: time.sleep(3-(time.time()-start)) #Sleep 1 - uběhlý čas (jeden loop = 3s)
            except: None
            if timer < 20: timer += 1 
            else: timer = 0 #Timer reset
            
    def voice_server():
        time.sleep(1)
        Voice_server.start()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler=handle_exit)
    print(f"\n\n -----------------------------------------\n\n    Smart Voice Assistent System ({VERSION}) \n            © Parma Industries\n\n -----------------------------------------\n\n")
    time.sleep(0.5)
    #multiprocessing.Process(target=Threads.autoupdate).start() #Autoupdate z githubu (Může být potřeba nastavení gitu)
    #time.sleep(1) #Tuhle a tu řádku nad tím jze odkomentovat, pokud nechcete automatické updaty z githubu
    tester.Tester.startup_test() #Test souborů
    time.sleep(1)
    multiprocessing.Process(target=Threads.tests).start() #Setup multiprocessingu
    multiprocessing.Process(target=Threads.data_update).start()
    multiprocessing.Process(target=Threads.voice_server).start()

""" Parma Industries """