# minecraft-bot-discord

implémentation d'un bot discord en python 

need to allow rcon port  :25575 

<ul>
  <li> l.13 : server ip</li>
  <li> l.14 : path to start.sh </li>
  <li> l.15 : port </li>
</ul>

<h3>start.sh :</h3>
<p>Create a shell file and put in the minecraft start command </p> 
```bash
java -Xmx1024M -Xms1024M -jar minecraft_server.1.20.2.jar nogui  
``` 
<br> 
<p>can be modified according to your server settings. Works on Forge and Vanilla</p>
<p>run main.py on a sudoer screen on linux <br> in the same directory as the server</p>

<h3>Need to install python module :</h3>
<ul>
  <li>discord.py : pip install discord.py</li>
  <li>mcstatus : pip install mcstatus </li>
  <li>mcrcon : pip install mcrcon</li>
  <li>subprocess : pip install subprocess</li>
  <li>shlex : pip install shlex</li>
</ul>

!help : to get the manual  <br>
!start : to start  the server <br>
!stop : to stop the server <br>
!status : to get status <br>
