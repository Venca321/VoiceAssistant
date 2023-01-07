
import configparser, os

class data():
    def write(location, section, option, data):
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigParser config
            file.read(location) #File read
            file.set(text_fix(section, False), text_fix(option, False), text_fix(data, False)) #Config parser write
            with open(location, "w") as configfile: file.write(configfile) #Uložení
            return True
        except: 
            try:
                file = configparser.ConfigParser(allow_no_value=True) #ConfigParser config
                file.read(location) #File read
                file.add_section(text_fix(section, False))
                file.set(text_fix(section, False), text_fix(option, False), text_fix(data, False)) #Config parser write
                with open(location, "w") as configfile: file.write(configfile) #Uložení
                return True
            except: return None

    def read(location, section, option):
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigParser config
            file.read(location) #File read
            output = text_fix(file.get(text_fix(section, False), text_fix(option, False)), True) #Získání dat
            return output
        except: return None

    def add_section(location, section):
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            file.add_section(text_fix(section, False)) #Add section
            with open(location, "w") as configfile: file.write(configfile) #Uložení
            return True
        except: return None

    def remove_section(location, section):
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            file.remove_section(text_fix(section, False)) #Remove section
            with open(location, "w") as configfile: file.write(configfile) #Uložení
            return True
        except: return None

    def remove_option(location, section, option):
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            file.remove_option(text_fix(section, False), text_fix(option, False)) #Remove option
            with open(location, "w") as configfile: file.write(configfile) #Uložení
            return True
        except: return None

    def sections(location):
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            output = []
            for i in file.sections(): output.append(text_fix(i, True)) #u všeho musí proběhnout text_fix
            return output
        except: return None

    def options(location, section):
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            output = []
            for i in file.options(text_fix(section, False)): output.append(text_fix(i, True)) #U všeho musí proběhnout text_fix
            return output
        except: return None

def text_fix(text, decode):
    list0 = ["//y// = ý", "//a// = á", "//i// = í", "//e// = é", "//u// = ú", "/e/ = ě", "/s/ = š", "/c/ = č", "/r/ = ř", "/z/ = ž", "\\n = \n", "/u/ = ů", "%% = %", "//U// = Ů", "//Y// = Ý", "//A// = Á", "//I// = Í", "//E// = É", "/E/ = Ě", "/S/ = Š", "/C/ = Č", "/R/ = Ř", "/Z/ = Ž", "/U/ = Ů"]
    for i in list0: #Pro věci v listu
        if decode == True: #Pokud má dekódovat 
            if i.split(" = ")[0] in text: 
                text = text.replace(i.split(" = ")[0], i.split(" = ")[1]) #1. část replacni tou 2.
        else:
            if i.split(" = ")[1] in text:
                text = text.replace(i.split(" = ")[1], i.split(" = ")[0]) #2. část replacni tou 1.
    return text

def match(text01, text02):
    best_score = 0 #Nejlepší score = 0
    text1 = text01
    text2 = text02
    for _ in range(2):
        text1 = text1.split(" ")
        same_letters = [] #Pozice stejných písmen list
        checked_letters = [] #Prověřená písmena list
        scores = [] #Score list
        score = 0 #Score = 0

        for i in text1: #i = jednotlivá slova
            for x in i: #x = jednotlivá písmena
                if not x in checked_letters: #Pokud tohle písmeno už není vypsané
                    for pos,char in enumerate(text2): #Získej písmena a jejich pozice v text2
                        if(char == x): #Pokud se písmeno shoduje s hledaným
                            checked_letters.append(x) #Zapiš, že už ho máme
                            same_letters.append(pos) #Zapiš jeho pozice (může jich být více)
                    
                for y in same_letters: #Vezmi jednotlivé pozice znaků, které se shodují
                    working_text2 = text2[y:] #2. text si vem jen od shodujícího se znaku
                    for w in text1: #Pro každé slovo v textu1
                        num1 = 0 #Proměná je 0
                        for z in w: #Pro každé písmeno ve slově (w)
                            try: #Pokus se
                                if z == working_text2[num1]: #Pokud se písmeno z textu1 i 2 shodují
                                    score += 1 #Zviš score
                            except: None #jinak nic
                            num1 += 1 #Proměná +1 (další písmeno)                      
                    scores.append(score) #List score                        
                same_letters.clear() #Vyčisti list

        for i in scores: #Pro každé score v listu
            x = (i / ((len(text01.replace(" ", "")) + len(text02.replace(" ", ""))) / 2))*100 #Vypočítat shodu slov ze score
            if x > best_score: #Pokud je aktuální score lepší, než to největší
                best_score = x #Přepiš největší score
        if best_score > 100: best_score = 100
        text1 = text02 #Prohození proměných text1 a text2
        text2 = text01 #...
    return best_score #Výstup

def match2(text1, text2): #Ve frázi text1 hledá slovo text2, vrátí pravděpodobnost výskytu
    text1 = text1.lower()
    text2 = text2.lower()
    chars_to_remove = data.options(f"{os.getcwd()}/Modules/engine/data/config.ini", "Characters to remove")
    for char in chars_to_remove: #Remove znaků z konfigu
        if char in text1: text1 = text1.replace(char, "")
        if char in text2: text2 = text2.replace(char, "")

    if not len(text1) > len(text2):
        text_ram = text2
        text2 = text1
        text1 = text_ram

    match = 0
    text1 = text1.split(" ") #Rozdělí na slova
    text2 = [x for x in text2] #Rozdělí na písmena
    for word in text1:
        word = [x for x in word] #Rozdělí na písmena
        



match2("ahojky, jak se máš?", "ahojky")