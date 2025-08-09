# MCOverseer

# Requierements
In server properties :
- enable rcon
- enable query
- enable status
- define rcon password
- define rcon port 25575

A start.sh file :
- with the appropriate commands to start your server
- with the x rules

A config.json :
like this
```
{
    "server_ip" : "127.0.0.1",
    "start_path" : "./start.sh",
    "api_key" : "your discord bot api_key",
    "my_discord_id" : your id for manage start/stop of your server with the bot
}
```


Module :
```
pip install mcrcon
pip install discord
pip install mcstatus
```
