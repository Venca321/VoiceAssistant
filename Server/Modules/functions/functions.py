
import configparser, os

class data():
    def write(location:str, section:str, option:str, data:str):
        """
        Zapíše do ini souboru location[str] do sekce section[str] nastavení option[str] o hodnotě data[str]
        """
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

    def read(location:str, section:str, option:str):
        """
        Returne hodnotu nastavení option[str] v sekci section[str], souboru location[str]
        """
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigParser config
            file.read(location) #File read
            output = text_fix(file.get(text_fix(section, False), text_fix(option, False)), True) #Získání dat
            return output
        except: return None

    def add_section(location:str, section:str):
        """
        Přidá sekci section[str] do souboru location[str]
        """
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            file.add_section(text_fix(section, False)) #Add section
            with open(location, "w") as configfile: file.write(configfile) #Uložení
            return True
        except: return None

    def remove_section(location:str, section:str):
        """
        Odstraní sekci section[str] v souboru location[str]
        """
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            file.remove_section(text_fix(section, False)) #Remove section
            with open(location, "w") as configfile: file.write(configfile) #Uložení
            return True
        except: return None

    def remove_option(location:str, section:str, option:str):
        """
        Odstraní nastavení optiont[str] v sekci section[str], souboru location[str]
        """
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            file.remove_option(text_fix(section, False), text_fix(option, False)) #Remove option
            with open(location, "w") as configfile: file.write(configfile) #Uložení
            return True
        except: return None

    def sections(location:str):
        """
        Returne sekce v souboru location[str]
        """
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            output = []
            for i in file.sections(): output.append(text_fix(i, True)) #u všeho musí proběhnout text_fix
            return output
        except: return None

    def options(location:str, section:str):
        """
        Returne nastavení v souboru location[str], sekci section[str]
        """
        try:
            file = configparser.ConfigParser(allow_no_value=True) #ConfigPasrser config
            file.read(location) #File read
            output = []
            for i in file.options(text_fix(section, False)): output.append(text_fix(i, True)) #U všeho musí proběhnout text_fix
            return output
        except: return None

def handle_exit(signum, frame): os._exit(1)

def text_fix(text:str, decode:bool):
    """
    Oprava textu text[str]
    """
    list0 = ["//y// = ý", "//a// = á", "//i// = í", "//e// = é", "//u// = ú", "/e/ = ě", "/s/ = š", "/c/ = č", "/r/ = ř", "/z/ = ž", "\\n = \n", "/u/ = ů", "%% = %", "//U// = Ů", "//Y// = Ý", "//A// = Á", "//I// = Í", "//E// = É", "/E/ = Ě", "/S/ = Š", "/C/ = Č", "/R/ = Ř", "/Z/ = Ž", "/U/ = Ů"]
    for i in list0: #Pro věci v listu
        if decode == True: #Pokud má dekódovat 
            if i.split(" = ")[0] in text: 
                text = text.replace(i.split(" = ")[0], i.split(" = ")[1]) #1. část replacni tou 2.
        else:
            if i.split(" = ")[1] in text:
                text = text.replace(i.split(" = ")[1], i.split(" = ")[0]) #2. část replacni tou 1.
    return text

class Texts():
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
                if reset_match: 
                    match = best_word_match
                    reset_match = False
                else: match = (match + best_word_match) / 2 #Průměrování aktuální shody
                    
            if match > output: output = match #Počítání největší shody 
        return output

    def best(file:str, text:str):
        """
        Fukce pro porovnání souboru ve tvaru (sekce Match): fce = ["neco", "neco]
        file = path/to/file.ini
        text = co v tom hledat
        """
        best_match_num = 0
        best_match = ""
        options = data.options(file, "Match") # Seber všechny možnosti, které se musí projít
        for function in options:
            posible_matches = data.read(file, "Match", function).split(", ") # Udělat list možností u jednotlivé fce
            actual_match = Texts.match(posible_matches, text) # Největší shoda pro tuhle fci
            if actual_match > best_match_num:
                best_match_num = actual_match # Zapamatuj největší shodu s fcí
                best_match = function

        return best_match_num, best_match[:1].upper()+best_match[1:]

    def match_in(file:str, text:str):
        """
        Fukce pro porovnání souboru ve tvaru (sekce Match): fce = neco, neco
        Ale hledá tyto možnosti v textu, což znamená, že "Kde je" má 100% shodu s "Kde je peněženka"
        """
        best_match_num = 0
        best_match = ""
        options = data.options(file, "Match") # Seber všechny možnosti, které se musí projít
        for function in options:
            posible_matches = str(data.read(file, "Match", function)).split(", ") # Udělat list možností u jednotlivé fce
            for posible_match in posible_matches:
                posible_matches_words = posible_match.split(" ")
                for word in posible_matches_words:
                    try: match = (match + Texts.match(text.split(" "), word))/2
                    except: match = Texts.match(text.split(" "), word)
                if match > best_match_num:
                    best_match_num = match
                    best_match = function
                match = None

        return best_match_num, best_match[:1].upper()+best_match[1:]
