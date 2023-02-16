
import mwxml, glob, csv, html2text

paths = glob.glob('wikidata/cswiki-latest-pages-articles*.xml*.bz2')

f = open('wikidata/wikidata.csv', 'w')
writer = csv.writer(f)
writer.writerow(["Page ID", "Title"])

def process_dump(dump, path):
    for page in dump:
        for revision in page:
            try:
                text = str(html2text.html2text(revision.text))
                text = text.replace("[[", "").replace("]]", "")
                
                yield page.id, page.title, text
            except: None

for page_id, title, text in mwxml.map(process_dump, paths):
    try:    
        writer.writerow([page_id, title])
        file = open(f"wikidata/pages/{page_id}.txt", "a")
        file.close()
        file = open(f"wikidata/pages/{page_id}.txt", "w")
        file.write(text)
        file.close()
    except: None

f.close()