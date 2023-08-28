import discord
from mcstatus import JavaServer
from mcrcon import MCRcon
import subprocess
import threading
import time
import shlex


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user.name}!')

@client.event
async def on_message(message):
    if message.content == '!status':
        await check_server_status(message.channel)
    if message.content == '!stop' :
        await server_stop(message.channel)
    if message.content == '!start' :
        await server_start(message.channel)
    if message.content == '!setup' :
        if threading.current_thread() == 0 :
            th = threading.Thread(target=stat, args=(message))
            th.daemon = True  # Terminer le thread lorsque le programme principal se termine
            th.start()
        else :
            await message.channel.send("le setup est déjà fait")
    if message.content == '!help' :
        await message.channel.send("!status : to get the server status \n!stop : to stop the server \n!start : to start the server \n!setup : pour setup l'auto actualisation")


async def server_start(channel) :
    subprocess.Popen(shlex.split("sudo path to start.sh"))
    await channel.send("Le serveur demarre ...")


async def server_stop(channel):
    server_ip = "your server ip"
    server_port = 25575  # Default RCON port
    rcon_password = "your rcon password"
    mcr = MCRcon(server_ip,"your rcon password")
    mcr.connect()
    mcr.command("stop")
    await channel.send("Le serveur s'eteint ...")


async def check_server_status(channel):

    try:
        server = JavaServer.lookup(server_ip + ':25565')
        status = server.status()


        server_ip = "your server ip"
        server_port = 25575  # Default RCON port
        rcon_password = "your rcon password"
        mcr = MCRcon(server_ip,rcon_password)
        mcr.connect()
        resp = mcr.command('/list')
        print(resp)

        msg = ""

        if status.players.online == 0 :
            msg = 'Nombre de joueur(s) en ligne : 0 '
        else :
            msg = 'Nombre de joueur(s) en ligne : ' + str(status.players.online) + "\n"
            p = resp[43:]
            p = p.split()
            for i in range(len(p)):
                msg += str(p[i]) + "\n"


        await channel.send('```🟩 Le serveur est en ligne ! \n' + msg + '```')
    except Exception as e:
        print("Server is offline or an error occurred:", e)
        await channel.send('🟥 Le serveur est hors ligne.')


def stat(message) :
    while True :
        time.sleep(60)
        check_server_status(message.channel)





client.run('your bot token')
