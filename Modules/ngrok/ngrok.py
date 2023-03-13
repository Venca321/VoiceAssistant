
import discord
from pyngrok import ngrok

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
        print(f" Ngrok running on {ip}\n")

    def start_ngrok():
        file = open("Modules/ngrok/data/ngrok.txt", "r")
        ngrok_token = file.read()
        file.close()

        ngrok.set_auth_token(ngrok_token)
        ssh_tunnel = ngrok.connect(5000, "http")
        ip = str(ssh_tunnel).split(" ")[1].replace('"', "")

        return ip

    client.run(TOKEN)