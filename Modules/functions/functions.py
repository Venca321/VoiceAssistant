
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

def match(search_in:list, search_for:str): #V listu stringů search_in hledá největší shodu s search_for, vrátí největší shodu %
    """
    Funkce pro match stringu s jedním z listu stringů (return %)
    search_in: list stringů (v kterých hledat)
    search_for: string (co hledat)
    """
    search_for = search_for.lower()
    chars_to_remove = data.options(f"{os.getcwd()}/Modules/engine/data/config.ini", "Characters to remove")
    for char in chars_to_remove: search_for = search_for.replace(char, "") #Remove znaků z konfigu

    text_ram = search_in
    search_in = []
    for working_text in text_ram: #Úprava všech stringů v listu (odebrání chars_to_remove)
        for char in chars_to_remove: working_text = working_text.replace(char, "")
        search_in.append(working_text.lower()) #Vložení upraveného zpět do search_in

    dict = {} #Dict písmen a pozicím k nim (dict["a"] = [0, 4])
    output, correct_letter_counter = 0, 0
    for potencial_match_raw in search_in:
        reset_match = True
        potencial_match = [x for x in potencial_match_raw]
        counter = 0
        for i in potencial_match: #Vytvoření dict
            try: dict[i] = dict[i] + [counter]
            except: dict[i] = [counter]
            counter += 1

        for search_for_word in search_for.split(" "):
            best_word_match = 0
            for offset in range(len(search_for_word)):
                updated_string = [x for x in search_for_word[offset:]]
                try: 
                    for start in dict[updated_string[0]]:
                        correct_letter_counter = 0
                        start = int(start)
                        counter = 0
                        for letter in updated_string:
                            try: 
                                if start+counter in dict[letter]: 
                                    correct_letter_counter += 1
                                    counter += 1
                            except: None
                            if counter > len(updated_string): break
                except: None
                if correct_letter_counter/len(search_for_word)*100 > best_word_match:
                    best_word_match = correct_letter_counter/len(search_for_word)*100

            if reset_match: match = best_word_match
            else: match = (match + best_word_match) / 2 #Průměrování aktuální shody
                
        if match > output: output = match #Počítání největší shody 
    return output