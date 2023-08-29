import discord
from mcstatus import JavaServer
from mcrcon import MCRcon
import subprocess
import shlex

#discord init
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#values 
server_ip = "your server ip"
start_path = 'sudo ' + 'path to start.sh' 
rcon_pass = "your rcon password"

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
    if message.content == '!help' :
        await message.channel.send("!status : to get the server status \n!stop : to stop the server \n!start : to start the server \n!setup : pour setup l'auto actualisation")


async def server_start(channel) :
    subprocess.Popen(shlex.split(start_path))
    await channel.send("Le serveur demarre ...")


async def server_stop(channel):
    mcr = MCRcon(server_ip,rcon_pass)
    mcr.connect()
    mcr.command("stop")
    await channel.send("Le serveur s'eteint ...")


async def check_server_status(channel):
    try:
        # query init 
        server = JavaServer.lookup(server_ip + ':25565')
        status = server.status()
        #rcon init
        mcr = MCRcon(server_ip,rcon_pass)
        mcr.connect()
        resp = mcr.command('/list')
        print(resp)

        msg = ""
        if status.players.online == 0 :
            msg = '  -   Player : 0 '
        else :
            msg = '  -  Player(s) : ' + str(status.players.online) + "\n"
            p = resp[43:]
            p = p.split()
            for i in range(len(p)):
                msg += str(p[i]) + "\n"
        embed=discord.Embed(title="Server status", description='🟩 Le serveur est en ligne ! \n' + msg, color=discord.Color.green())
        await channel.send(embed=embed)
    except Exception as e:
        print("Server is offline or an error occurred:", e)
        embed=discord.Embed(title="Server status", description='🟥 Le serveur est hors ligne', color=discord.Color.red())
        await channel.send(embed=embed)
        


client.run(
  'MTEyNDMxNzc3ODkzMzk4NTMxMQ.GDFrRh.O8YY7z2_MeURIMVA4ktaCvojrsb_RrNg4r2RWc')
