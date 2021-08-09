```
└─# gobuster dir -u https://gobustme.ctflearn.com/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://gobustme.ctflearn.com/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2021/08/09 02:40:05 Starting gobuster in directory enumeration mode
===============================================================
/sex                  (Status: 301) [Size: 169] [--> http://gobustme.ctflearn.com/sex/]
/flag                 (Status: 301) [Size: 169] [--> http://gobustme.ctflearn.com/flag/]
/skin                 (Status: 301) [Size: 169] [--> http://gobustme.ctflearn.com/skin/]
/shadow               (Status: 301) [Size: 169] [--> http://gobustme.ctflearn.com/shadow/]
/call                 (Status: 301) [Size: 169] [--> http://gobustme.ctflearn.com/call/]  
/hide                 (Status: 301) [Size: 169] [--> http://gobustme.ctflearn.com/hide/]  
Progress: 16920 / 220561 (7.67%)
```
`/hide` contains the flag.

![gobustmeflag](https://user-images.githubusercontent.com/59718043/128655554-cd33619d-640a-47ea-b96b-cfb2c389e153.png)
