import discord
from discord.ext import commands
from mcstatus import JavaServer
from mcrcon import MCRcon
import subprocess
import shlex
import json
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de Discord
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

# Chargement de la configuration
try :
    with open("config.json","r") as f:
        config = json.loads("".join(f.readlines()))
except Exception as e:
    logger.error(f"Erreur lors du chargement de la configuration : {e}")
    config = {}

# Chargement des données
try :
    with open("data.json","r") as f :
        data = json.loads("".join(f.readlines()))
except Exception as e:
    logger.error(f"Erreur lors du chargement des données : {e}")
    data = {}


@client.event
async def on_ready():
    logger.info(f'Connecté en tant que {client.user.name}!')
        
async def save_data():
    try:
        with open("data.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des données : {e}")
    
@client.command()
async def start(ctx):
    if ctx.author.id != config["my_discord_id"]:
        return
    try:
        with open("log", "w") as out:
            process = subprocess.Popen(shlex.split(config["start_path"]), stdout=out)
            await ctx.channel.send("Le serveur démarre ...")
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du serveur : {e}")
        await ctx.channel.send("Une erreur est survenue lors du démarrage du serveur.")
        
@client.command()
async def stop(ctx):
    if ctx.author.id != config["my_discord_id"]:
        return
    try:
        mcr = MCRcon(config["server_ip"], config["rcon_pass"])
        mcr.connect()
        mcr.command("stop")
        await ctx.channel.send("Le serveur s'éteint ...")
    except Exception as e:
        logger.error(f"Erreur lors de l'arrêt du serveur : {e}")
        await ctx.channel.send("Une erreur est survenue lors de l'arrêt du serveur.")
    
@client.command()
async def status(ctx):
    try:
        mcr = MCRcon(data[str(ctx.guild.id)]["ip"], data[str(ctx.guild.id)]["rcon_pass"])
        mcr.connect()
        players = mcr.command('/list')[43:].split()
        nb_player = len(players)
        msg = f"Players : {nb_player}\n" + "\n".join(players) if nb_player >= 1 else f"Player : {nb_player}"
        embed = discord.Embed(title="Server status", description=f'🟩 Le serveur est en ligne ! \n{msg}', color=discord.Color.green())
        await ctx.channel.send(embed=embed)
    except Exception as e:
        logger.error(f"Erreur lors de la vérification du statut du serveur : {e}")
        embed = discord.Embed(title="Server status", description='🟥 Le serveur est hors ligne', color=discord.Color.red())
        await ctx.channel.send(embed=embed)

@client.command()
async def MChelp(ctx):
    await ctx.channel.send("!setupChannel : pour parametre le channel comme celui du bot\n!register [ip] [rcon_password] : pour enregistrer un serveur minecraft\n!info : pour avoir les information du serveur enregistrer")

@client.command()
async def register(ctx, ip=None, rcon=None):
    guildId = str(ctx.guild.id)
    if guildId in data.keys() :
        if ctx.channel.id == data[guildId]["channel"] or is_owner(ctx) :
            server = data[guildId]
            server["ip"] = ip
            server["rcon"] = rcon
            server["motd"] = "A minecraft server"
            server["version"] = "undefinned"
            server["bedrock"] = "undefinned"
            await ctx.channel.send(embed=discord.Embed(title="Enregistrement reussi", description=f"L'ip est définie à : {server["ip"]}\nPour plus d'informations !info"))
            await ctx.message.delete()
            await save_data()
        else :
            await ctx.channel.send(embed=discord.Embed(title="Erreur",description="vous n'avez pas permissions pour faire cceci dans ce channel"))
    else :
        await ctx.channel.send(embed=discord.Embed(title="Erreur d'enregistrement",description="Il faut d'abord `!setupCHannel`"))
        
@client.command()
async def setupChannel(ctx,channel=None):
    guildId = str(ctx.guild.id)
    if guildId in data.keys() :
        if ctx.channel == data[guildId]["channel"] or is_owner(ctx):
            data[guildId]["channel"] = channel
        else :
            await ctx.channel.send(embed=discord.Embed(title="Erreur",description="Pour modifier le channel, il faut envoyer la modification depuis l'ancien channel"))
            return
    else :
        if channel is None :
            channel = ctx.channel
        data[guildId]= {}
        data[guildId]["channel"] = channel.id
    await channel.send(embed=discord.Embed(title="Modification channel",description="reussie"))
    await save_data()
        
@client.command()
async def info(ctx):
    # check if the server register a channel
    if str(ctx.guild.id) not in data.keys() :
            await ctx.channel.send(embed=discord.Embed(title="Erreur d'enregistrement",description="Il faut d'abord `!setupCHannel`"))
            return
        
    # check if the server register ip and rcon password
    if "ip" not in data[str(ctx.guild.id)].keys() :
        await ctx.channel.send(embed=discord.Embed(title="Erreur d'enregistrement",description="Il faut d'abord `!register`"))
        return
    
    # select sever data
    server = data[str(ctx.guild.id)]
    
    #get the status data
    try:
        server_ip = server["ip"]
        javaServer = JavaServer.lookup(server_ip + ':25565')
        status = javaServer.status()
    except Exception as e:
        status = None
    
    #check connection and refresh data
    connected = status is not None
    if connected :
        server["version"] = status.version.name
        server["bedrock"] = status.motd.bedrock
        server["motd"] = status.motd.parsed[0]
    
    #write the message
    description = f"**{ctx.guild.name}**\n{server["motd"]}\n\n"
    description += f"- IP : `{server["ip"]}` \n"
    description += f"- Status : ̀` {"online" if connected else "offline"}` \n"
    description += f"- Version : `{server["version"]}` \n"
    description += f"- Bedrock allowed : `{server["bedrock"]}` \n"
    
    #create embed
    embed = discord.Embed(title="Server information",description= description)
    
    #configure icon
    if connected and status.icon is not None :
        embed.set_image(status.icon)
        
    if connected :
        embed.color = discord.Color.green()
    else :
        embed.color = discord.Color.red()
        
    #flush
    await ctx.channel.send(embed=embed)
    
def is_owner(ctx,member=None):
    if member is None : member = ctx.author
    return ctx.author == ctx.guild.owner

client.run(config["api_key"])
