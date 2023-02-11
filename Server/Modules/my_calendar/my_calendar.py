
from Modules.functions.functions import *
from bs4 import BeautifulSoup as Soup
import datetime, requests, os

class Match():
    def match(text, output=False):
        out = Texts.best(f"{os.getcwd()}/Modules/my_calendar/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update(timer):
        pass

class Calendar():
    def check_changes():
        pass

    def rozvrh_supl(den):
        day = (datetime.datetime.today()+datetime.timedelta(days=int(den))).strftime("%y%m%d") #Datum na určený den
        dayweek = str((datetime.datetime.today()+datetime.timedelta(days=int(den))).weekday()) #Den v týdnu
        weeknumber = str((datetime.datetime.today()+datetime.timedelta(days=int(den))).isocalendar()[1])
        if (int(weeknumber) % 2) == 0: sudy = 1
        else: sudy = 0

        if dayweek == "5" or dayweek == "6": 
            return None
        else:
            url = f"https://www.glouny.cz/suplovani/su{day}.htm" #Url suplování
            r = requests.get(url)
            soup = Soup(r.content, "html.parser")
            text = (soup.findAll("td", {"class": "td_supltrid_3"})) #Získání nepřehledných dat o suplování

            uz = False
            output = ""
            for i in text: #Vezmeme to postupně
                out = i.find("p") #Nalezneme všechen text
                if out: #Pokud není None
                    out = str(out)[3:-4] #Odebereme <p>...</p>
                    if out.startswith("  "): #Pokud začíná 2ma mezerami tak je to název třídy...
                        out = out.replace("  ", "") #Odebrání mezer
                        if out == data.read(f"{os.getcwd()}/Modules/calendar/data/config.ini", "Settings", "trida"): uz = True #Pokud je to naše třída, tak uz = True
                        else: uz = False #Jinak uz = False (pokud zkončí naše třída, tak je tohle důležité)
                    elif uz: #Pokud je naše třída, tak zapisuj output
                        if "." in out: output = output + ",, " + out #Pokud obsahuje tečku (jako 3. hodina...), tak rozděl 2ma čárkami
                        else: output = output + ", " + out #Jinak rozděl normálně jednou čárkou
            output = output[3:] #Odebrání ",, " na začátku
            output = output.split(",, ") #Rozdělení po dvou čárkách (po hodinách)

            output1 = ""
            for w in output:
                if "&gt;&gt;" in w or "&lt;&lt;" in w: #Pokud je v suplování přesun, tak fixni bug, který to rozděloval na 2 řádky
                    output1 += w + " "
                else:
                    output1 += w + ",,, " #Jinak to nech, jak to bylo

            output = (output1[:-4]).split(",,, ") #...

            hod = 0 #Nastavení proměných
            end_rozvrh = "" #Výstupní rozvrh
            akce_info = False
            info = "" #Informace k rozvrhu
            rozvr = data.read(f"{os.getcwd()}/Modules/calendar/data/config.ini", dayweek, "rozvrh").split(", ") #List předmětů
            ucitele = data.read(f"{os.getcwd()}/Modules/calendar/data/config.ini", dayweek, "ucitele").split(", ") #List učitelů
            actual_hour = -1
            for x in rozvr: #Postupně pro všechny předměty na daný den
                actual_hour += 1
                if "/" in x and sudy == 1: #Pokud je sudý týden a je v tom / tak použij to, co je nastavené na sudý týden
                    z = data.read(f"{os.getcwd()}/Modules/calendar/data/config.ini", "Settings", "sudy").split(", ")
                    for w in z:
                        if w in x:
                            x = w
                elif "/" in x and sudy == 0: #Pokud je lichý týden --""--
                    z = data.read(f"{os.getcwd()}/Modules/calendar/data/config.ini", "Settings", "lichy").split(", ")
                    for w in z:
                        if w in x:
                            x = w

                num = 0
                for i in output:
                    num += 1
                    #if x in i and f"{hod}.hod" in i and ucitele[hod] in i: #Pokud najdeš změnu pro tuhle hodinu, předmět a učitele, tak:
                    if f"{hod}.hod" in i and ucitele[hod] in i or x in i and f"{hod}.hod" in i: #Pokud najdeš změnu pro tuhle hodinu a učitele nebo pro tuhle hodinu a předmět, tak:
                        if "odpadá" in i:
                            if actual_hour+1 == len(end_rozvrh.split(", ")):
                                end_rozvrh = end_rozvrh + (", *---*") #Pokud hodina odpadá
                        
                        elif "supluje" in i:
                            i = i.split(", ") #Rozdělit
                            end_rozvrh = end_rozvrh + (f', *{i[1]}*') #Předmět který se supluje, přidej do rozvrhu
                            info += f", {str(hod)}.hod {i[1]}, supluje {i[4]} {i[5]}" #Print do info zprávy

                        elif "přesun" in i: #Pokud se hodina posouvá
                            if "&gt;&gt;" in i:
                                info += f', {i.replace("&gt;&gt; ", "")}' #Print do info zprávy
                                end_rozvrh = end_rozvrh.split(", ") #Rozděl rozvrh
                                num1, end_rozvrh1 = 0, "" #Proměnné
                                for t in end_rozvrh: #Pro každé v rozvrhu
                                    if int(i[-5:-4]) == num1-1: #Pokud je to ta hodina, kam se posouvá
                                        end_rozvrh1 += f', *{i.split(", ")[1]}*' #Přidej tam onu přesunutou hodinu
                                    elif not int(i[-5:-4]) == num1-1: #Pokud to není ta hodina, nech tam, co tam je
                                        end_rozvrh1 += ", " + t #...
                                    num1 += 1
                                end_rozvrh = end_rozvrh1[2:] #Odstranění ", "
                                end_rozvrh += (", *---*") #Přidání volné hodiny místo té, která se přesunula

                        elif "změna" in i: #Pokud je změna
                            if "(" in i.split(", ")[3]: #Pokud by bylo číslo učebny špatně posunuté
                                info += f", {str(hod)}.hod {x} změna {i.split()[3]}" #Dej do infa číslo hodiny, změna (číslo učebny)
                            else:
                                info += f", {str(hod)}.hod {x} změna {i.split()[2]}" #Dej do infa číslo hodiny, změna (číslo učebny)

                        elif "spojí" in i:
                            end_rozvrh = end_rozvrh + (f', *{i.split(", ")[1]}*') #Spojení hodin
                            info += f", {str(hod)}.hod spojeno ({i.split(', ')[5]})"

                        elif "výměna" in i: 
                            info += f", {i}" #Print do info zprávy
                        
                        else: 
                            end_rozvrh = end_rozvrh + (", "+x) #Pokud je neznámá změna
                            print(x, i)

                    elif num == len(output): 
                        if actual_hour+1 == len(end_rozvrh.split(", ")):
                            end_rozvrh = end_rozvrh + (", "+x) #Pokud není změna

                if "akce školy" in i: #Pokud je akce školy, tak to dej do infa
                    if not akce_info:
                        try: 
                            int(i[:5].replace("., ", ""))
                            info += f', {i[:5].replace("., ", "-")}. hod akce školy' #Např.: 3-4. hod akce školy
                            akce_info = True
                        except:
                            info += f', akce školy' #Např.: 3-4. hod akce školy
                            akce_info = True

                hod += 1
            end_rozvrh = end_rozvrh[2:] #Odeber ", " na začátku
            info = info[2:].replace(",,", ",") #Odeber ", " na začátku

            num = 10
            go = True
            now = False
            work_rozvrh = [] #Odendání odpadlých hodin na konci rozvrhu
            while go: #Jdi od zádu
                try:
                    if end_rozvrh.split(", ")[num] == "---" or end_rozvrh.split(", ")[num] == "*---*": #Pokud je to odpadlá hodina
                        if now: work_rozvrh.append(end_rozvrh.split(", ")[num]) #A už jsi narazil na předmět, tak jí tam dej
                    else: 
                        now = True
                        work_rozvrh.append(end_rozvrh.split(", ")[num]) #Pokud není odpadlá, tak jí tam dej
                except: None
                if num == 0: go = False #Pokud dojdeš na konec, ukonči smičku
                else: num -= 1

            work_rozvrh1 = work_rozvrh #Obrať pořadí věcí v listu
            work_rozvrh = [] #...
            num = len(work_rozvrh1)-1 #...
            for i in work_rozvrh1:
                work_rozvrh.append(work_rozvrh1[num])
                num -= 1

            num = 0
            list1 = []
            for x in work_rozvrh: #Získej lokace všech zbylích volných hodin v listu
                if x == "---" or x == "*---*":
                    list1.append(num) #Hoď to do listu1
                num += 1
            list2 = data.read(f"{os.getcwd()}/Modules/calendar/data/config.ini", "Settings", "hod").split(", ") #List2 je seznam časů hodin

            for i in range(11): #Odebrání prvních volných hodin z listu
                if not i in list1: #...
                    break #...
                else:
                    list1.remove(i)

            start = str(list2[i]).split("___")[0] #Začátek školy
            end = str(list2[len(work_rozvrh)-1]).split("___")[1] #Konec školy

            list3 = [] #List3 jsou všechny volné hodiny, které nejsou na začátku nebo na konci
            for i in list1:
                list3.append(list2[i])
                
            obed = ", ".join(list3)

            if info[-1:] == ",": #Pokud je poslední čárka
                info = info[:-1] #Odeber ji
            
            return end_rozvrh, info, f"{start}___{end}", obed #Vrať to