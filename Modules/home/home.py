
from requests_html import HTMLSession
from bs4 import BeautifulSoup as Soup
from Modules.functions.functions import *
from proxmoxer import ProxmoxAPI
import os, json

class Match():
    def match(text):
        return 99

class Data():
    def update(timer):
        if timer % 2 == 0: Octoprint.update() #Updatují se nastřídačku, aby to nespomalovalo systém
        if timer % 2 == 1: Tasmota.update()
        if timer % 3 == 0: Proxmox.update()

class Proxmox():
    def update():
        try: proxmox = ProxmoxAPI(data.read(f"{os.getcwd()}/Modules/home/data/config.ini", "Proxmox", "ip"), user="API@pve", password="VoiceAssistant", verify_ssl=False) #Proxmox login...
        except: 
            for i in data.sections(f"{os.getcwd()}/Modules/home/data/data.ini"):
                if "proxmox" in i.lower():
                    data.write(f"{os.getcwd()}/Modules/home/data/data.ini", i, "status", "offline")
                    if not i == "Proxmox": data.write(f"{os.getcwd()}/Modules/home/data/data.ini", i, "name", "---")
                    data.write(f"{os.getcwd()}/Modules/home/data/data.ini", i, "cpu", "---")
                    data.write(f"{os.getcwd()}/Modules/home/data/data.ini", i, "ram", "---")
                    data.write(f"{os.getcwd()}/Modules/home/data/data.ini", i, "uptime", "---")
            return

        for i in proxmox.nodes.get():
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Proxmox", "status", i["status"])
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Proxmox", "cpu", str(float(i["cpu"])*100)) #Převedení do %
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Proxmox", "ram", str(float(i["mem"])/float(i["maxmem"])*100 )) #Převedení do %
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Proxmox", "uptime", str(float(i["uptime"])/3600 )) #Převednení do hodin

        vmids = []
        for i in proxmox.get("nodes/proxmox/qemu"):
            vmids.append(f'proxmox_vmid{i["vmid"]}')
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", f'proxmox_vmid{i["vmid"]}', "status", i["status"])
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", f'proxmox_vmid{i["vmid"]}', "name", i["name"])
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", f'proxmox_vmid{i["vmid"]}', "cpu", str(float(i["cpu"])*100)) #Převedení do procent
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", f'proxmox_vmid{i["vmid"]}', "ram", str(float(i["mem"])/float(i["maxmem"])*100)) #Převedení do procent
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", f'proxmox_vmid{i["vmid"]}', "uptime", str(float(i["uptime"])/3600)) #Převendení do hodin

        for i in data.sections():
            if "proxmox_vmid" in i and not i in vmids: #Pokud tento VM už neexistuje smaž sekci
                data.remove_section(f"{os.getcwd()}/Modules/home/data/data.ini", i)

class Octoprint():
    def update():
        octoprint_ip = data.read(f"{os.getcwd()}/Modules/home/data/config.ini", "Octoprint", "ip") #Získání IP
        s = HTMLSession()
        url = f"http://{octoprint_ip}/api/connection?apikey=3D402F19D3F742518BD31B0FE3EA5CF2"
        try: 
            r = s.get(url, timeout=1) #Pokud se můžeš připojit vem data
            soup = str(Soup(r.text, "html.parser"))
            out = json.loads(soup)
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "status", out["current"]["state"]) #Zapsání stavu do souboru
            online = True
        except: 
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "status", "Offline") #Pokud ne tak je to offline
            online = False

        if online:
            s = HTMLSession()
            url = f"http://{octoprint_ip}/api/job?apikey=3D402F19D3F742518BD31B0FE3EA5CF2"
            try:    
                r = s.get(url, timeout=1) #Scrap dalších informací
                soup = str(Soup(r.text, "html.parser"))
                out = json.loads(soup)
                data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "fileName", out["job"]["file"]["name"]) #Zapsání dat do souboru
                data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "printTimeLeft", str("{:.2f}".format(float(out["progress"]["printTimeLeft"])/60)))
                data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "printTime", str("{:.2f}".format(float(out["progress"]["printTime"])/60)))
                data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "printPercent", str(float("{:.2f}".format(float(data.get("Octoprint", "printTime"))/(float(data.get("Octoprint", "printTime"))+float(data.get("Octoprint", "printTimeLeft")))*100))))
            except: 
                data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "fileName", "---") #Zapsání dat do souboru
                data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "printTimeLeft", "---")
                data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "printTime", "---")
                data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Octoprint", "printPercent", "---")

class Tasmota():
    def update():
        tasmota_ip = data.read(f"{os.getcwd()}/Modules/home/data/config.ini", "Tasmota", "ip") #Získání IP
        s = HTMLSession()
        url = f"http://{tasmota_ip}/cm?cmnd=Power" 
        try:    
            r = s.get(url, timeout=1) #Scrap informací
            soup = str(Soup(r.text, "html.parser"))
            out = (json.loads(soup))["POWER1"].lower() #Vybrání pouze pro mě zajímavé hodnoty
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Tasmota", "status", "Online") #Zapsání hodnoty do souboru
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Tasmota", "power", out)
        except: 
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Tasmota", "status", "Offline") #Zapsání hodnoty do souboru
            data.write(f"{os.getcwd()}/Modules/home/data/data.ini", "Tasmota", "power", "---")