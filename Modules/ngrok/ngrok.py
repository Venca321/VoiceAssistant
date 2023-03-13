
import os, json, time, discord, sys

def discord_status():
    FILE = "Modules/ngrok/tunnels.json"
    token_file = open("Modules/ngrok/data/token.txt")
    TOKEN = token_file.read()
    token_file.close()

    client = discord.Client()

    @client.event
    async def on_ready():
        ip = start_ngrok()
        channel = client.get_channel(1084757107447975956)
        await channel.send(f"@here Server restarted, now is on:\n{ip}")

        for _ in range(3): #Vymaže ten curl print, který nenávidím
            sys.stdout.write("\033[F")
            print(" "*100)
            sys.stdout.write("\033[F")

        print(f" Ngrok running on {ip}\n")

    def start_ngrok():
        os.system("ngrok http 5000 &")
        time.sleep(3)
        os.system(f"curl  http://localhost:4040/api/tunnels > {FILE}")

        with open(FILE) as data_file: datajson = json.load(data_file)
        for i in datajson['tunnels']: ip = i['public_url']
        os.remove(FILE)

        return ip

    client.run(TOKEN)