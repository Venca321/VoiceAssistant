
from Modules.functions.functions import *

class Match():
    def match(text, output=False):
        out = Texts.best(f"{os.getcwd()}/Modules/my_math/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update(timer):
        pass

class Calculator(): # Tohle chce celé předělat -----------------------------------------------------
    def calculate(text):
        text = text.lower().replace("_", "") #Odebrání mezer
        replacement_num = ["nula // 0", "nultou // 0", "nuly // 0", "jedna // 1", "první // 1", "jedné // 1", "jedný // 1", "dva // 2", "druhou // 2", "dvou // 2", "tři // 3", "třetí // 3", "tří // 3", "čtyři // 4", "čtvrtou // 4", "čtyř // 4", "pátou // 5", "pěti // 5", "pět // 5", "šestou // 6", "šesti // 6", "šest // 6", "sedmou // 7", "sedmi // 7", "sedm // 7", "osmou // 8", "osmi // 8", "osm // 8", "devět // 9", "devátou // 9", "devíti // 9", "desátou // 10", "deseti // 10", "desíti // 10", "deset // 10"]
        for i in replacement_num: #Nahrazení slov číslem
            i = i.split(" // ")
            text = text.replace(i[0], i[1])

        replacement = ["x // *", "krát // *", "děleno // /", "plus // +", "mínus // -", "na2 // **2", "na3 // **3", "na4 // **4", "na5 // **5", "na6 // **6", "na7 // **7", "na8 // **8", "na9 // **9", "na10 // **10"]
        for i in replacement: #Nahrazení slov matematickou operací
            i = i.split(" // ")
            text = text.replace(i[0], i[1])

        replacement2 = ["2odmocninaz // **(1/2)", "3odmocninaz // **(1/3)", "4odmocninaz // **(1/4)", "5odmocninaz // **(1/5)", "6odmocninaz // **(1/6)", "7odmocninaz // **(1/7)", "8odmocninaz // **(1/8)", "9odmocninaz // **(1/9)", "10odmocninaz // **(1/10)", "odmocninaz // **(1/2)"]
        for i in replacement2: #Nahrazení slov m. operací
            i = i.split(" // ")
            if i[0] in text:
                text = text.replace(i[0], "")
                text = text.replace("e", "") #Odmocnina z = Odmocnina ze
                text = text+i[1]

        try: 
            print(text) ###############################################################
            output = str(eval(text)) # 3+4 = 7 --> ze stringu počítá
            if output[-2:] == ".0": output = output[:-2] #Pokud jsou poslední 2 znaky .0 odeber je  
            return output
        except: 
            print("Error calculating:", text) #####################################
            ####### Pravděpodobně v budoucnu return "Error" / None, abych s tím mohl dále pracovat