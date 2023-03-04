
from Modules.functions.functions import *
from multiprocessing.pool import ThreadPool
import wikipedia, os, csv, time

class Wiki():
    def web_find(text:str):
        """
        Najde v textu klíčová slova, které najde na wikipedii, pokud dosáhne dostatečné shody, vrátí to
        """
        remove_from_input = data.read(f"{os.getcwd()}/Modules/web_finder/data/vocabulary.ini", "Wiki_remove", "remove_from_input").split(", ")
        remove_from_output = data.read(f"{os.getcwd()}/Modules/web_finder/data/vocabulary.ini", "Wiki_remove", "remove_from_output").split(", ")

        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(remove_from_input, checked_word) > 90:
                text = text.replace(checked_word, "").replace("  ", " ")
        if text.startswith(" "): text = text[1:]
        
        wikipedia.set_lang("cs") #Wikipedie CS
        page = wikipedia.search(text) #Stránky
        if Texts.match([page[0]], text) >= 80: #Checkout zda title stránky má s texten shodu větší, než 80%
            output = wikipedia.summary(page[0]).split("\n")[0] #Obsah
            
            for checked_word in output.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
                if Texts.match(remove_from_output, checked_word) > 90:
                    output = output.replace(checked_word, "").replace("  ", " ")

            return output

    def wikidata_find(text:str, odstavcu:int=1):
        """
        Najde v textu klíčová slova, které najde v lokálních souborech (zpracovaná data z wikipedie), pokud dosáhne dostatečné shody, vrátí to
        """
        remove_from_input = data.read(f"{os.getcwd()}/Modules/web_finder/data/vocabulary.ini", "Wiki_remove", "remove_from_input").split(", ")
        remove_from_output = data.read(f"{os.getcwd()}/Modules/web_finder/data/vocabulary.ini", "Wiki_remove", "remove_from_output").split(", ")

        for checked_word in text.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
            if Texts.match(remove_from_input, checked_word) > 90:
                text = text.replace(checked_word, "").replace("  ", " ")
        if text.startswith(" "): text = text[1:]

        pool = ThreadPool(processes=5)

        async_result1 = pool.apply_async(Wiki.wikidata_reader, ("Data/wikidata/wikidata1.csv", text, odstavcu))
        async_result2 = pool.apply_async(Wiki.wikidata_reader, ("Data/wikidata/wikidata2.csv", text, odstavcu))
        async_result3 = pool.apply_async(Wiki.wikidata_reader, ("Data/wikidata/wikidata3.csv", text, odstavcu))
        async_result4 = pool.apply_async(Wiki.wikidata_reader, ("Data/wikidata/wikidata4.csv", text, odstavcu))
        async_result5 = pool.apply_async(Wiki.wikidata_reader, ("Data/wikidata/wikidata5.csv", text, odstavcu))

        out1 = async_result1.get()
        out2 = async_result2.get()
        out3 = async_result3.get()
        out4 = async_result4.get()
        out5 = async_result5.get()

        out = [out1, out2, out3, out4, out5]
        for output in out:  
            if output:
                for checked_word in output.split(" "): #Pokud je nějaké slovo na 90%+ in words_to_remove, odeber ho
                    if Texts.match(remove_from_output, checked_word) > 90:
                        output = output.replace(checked_word, "").replace("  ", " ")

                return output

    def wikidata_reader(path_to_wikidata_file:str, text:str, odstavcu:int):
        wikidata = csv.reader(open(path_to_wikidata_file, "r"))
        for row in wikidata:
            if row[1].lower() == text:
                file = open(f"Data/wikidata/pages/{row[0]}.txt", "r")
                output = file.read()
                file.close()

                out = output.split("\n")
                output = ""
                try:
                    for i in range(odstavcu):
                        if len(out[i]) < 25: out.remove(out[i])
                        text = out[i]
                        if text.endswith(" "): text = text[:-1]
                        if text.endswith(" ="): text = text[:-2]
                        if text.startswith(" "): text = text[1:]
                        output = output + "\n" + text
                except: None

                if output.startswith("\n"): output = output[1:]
                return output
        return None

class Google:
    def find():
        pass
