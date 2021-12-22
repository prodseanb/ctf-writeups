# CTF - [THM Solar, exploiting log4j](https://tryhackme.com/room/solar)
Nmap scan:
```
PORT     STATE SERVICE
22/tcp   open  ssh
111/tcp  open  rpcbind
8983/tcp open  unknown
```

Port 8983 is interesting, navigating to the web server on this port, I found a web app running Apache Solr version 8.11.0. Apparently, this software is known to 
have the vulnerable log4j package.
<br/><br/>
![Screenshot from 2021-12-22 13-53-37](https://user-images.githubusercontent.com/59718043/147141427-ae530fa8-811d-4d3a-a664-ab908b62025e.png)

The dashboard shows indicators that the log4j package is used for the logging activity on this application.
```
-Dsolr.log.dir=/var/solr/logs
```
This machine is supplied with example log files for investigation. In one of the log files, `solr.log`, there are multiple entries of the same requests pointing to
one specific URL endpoint or path. This path is set to `/admin/cores`. Another interesting field is the `params={}`, which we can supply with user input.

```
TO BE CONTINUED
```
