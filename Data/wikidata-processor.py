
"""
Script pro zpracování dat z wikipedie na použitelná wikidata, s kterými pracuje hlasový asistent 
!!! Na mém Pc běželo zhruba 45 minut (dejte tomu čas) !!!
"""

try:
    import mwxml, glob, csv, html2text, re, time
except:
    import os
    os.system("pip install mwxml")
    os.system("pip install html2text")
    import mwxml, glob, csv, html2text, re, time

paths = glob.glob('wikidata/cswiki-latest-pages-articles*.xml*.bz2') #Načtení wiki dat (staženo z wikipedie)

f = open('wikidata/wikidata.csv', 'w') #Zapsání co řádky znamenají
writer = csv.writer(f)

start = time.time()
print("Started")

def process_dump(dump, path):
    for page in dump:
        for revision in page:
            global errors
            try:
                text = str(html2text.html2text(revision.text))
                text = text.replace("'''", "").replace("''", "").replace("\n", " ") #Odstranění Spousty nepotřebných věcí

                founds = re.findall(r"!mark!(.*?)!/mark!", text.replace("[[", "!mark!").replace("]]", "!/mark!"))
                for found in founds: 
                    if "Soubor:" in found: text = text.replace(found, "")
                    else:
                        try: text = text.replace(found, found.split("|")[-1])
                        except: None
                    text = text.replace("[[", "").replace("]]", "")

                founds = re.findall("{{Infobox (.*?) }}", text)
                for found in founds: text = text.replace(f"{{Infobox {found} }}", "")

                found = text.find("Externí odkazy ==")
                if found: text = text.replace(text[found:], "")

                founds = re.findall(r"{{(.*?)}}", text)
                for found in founds: text = text.replace(found, "").replace("{", "").replace("}", "")

                founds = re.findall(r"== (.*?) ==", text)
                for found in founds: text = text.replace(f"== {found} ===", f"-----///{found}///").replace(f"== {found} ==", f"-----///{found}///")

                out = []
                for i in text.split("-----"): #Odstranění nepotřebných sekcí
                    y = i
                    y = y.lower().replace("-", "").replace(" ", "").replace("=", "")
                    if "///reference///" in y or "///literatura///" in y or "///souvisejícíčlánky///" in y or "///poznámky///" in y or "///odkazy///" in y: pass
                    else: out.append(i.replace("///", ""))

                text = "\n".join(out)
                text = text.replace("  ", "")

                yield page.id, page.title, text
            except: errors += 1

banned_words = ["leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen", "září", "říjen", "listopad", "prosinec", "ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince", "století"]
aproved = 0
banned = 0
errors = 0
last_printed = 0
for page_id, title, text in mwxml.map(process_dump, paths):
    try:
        percentage = aproved / 1100
        if percentage.is_integer() and not percentage == last_printed: 
            last_printed = percentage
            print(f"Probíhá zpracování dat ({percentage}%)")

        process = True
        if page_id == 4 or page_id == 7 or page_id == 8:  process = False

        for i in banned_words: #Tohle vyřadí měsíce, dny a další stránky, které nepotřebuji
            for word in title.split(" "):
                if i == word: process = False

        try:
            int(title) #Tohle odstraní všechny stránky s názvem pouze čísla (převážně roky / informace o číslech - není potřeba)
            process = False
        except: None
            
        if process:
            writer.writerow([page_id, title])
            file = open(f"wikidata/pages/{page_id}.txt", "a")
            file.close()
            file = open(f"wikidata/pages/{page_id}.txt", "w")
            file.write(text)
            file.close()
            aproved += 1
        else: banned += 1
    except: errors += 1

f.close()
print(f"Dokončeno v čase {(time.time()-start)/60}min")
print(f"Zpracováno: {aproved+banned} stránek\nUloženo: {aproved} stránek\nOdstraněno: {banned} stránek\nErrorů: {errors}")