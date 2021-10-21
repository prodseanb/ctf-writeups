# CTF - [Delivery](https://app.hackthebox.eu/machines/Delivery)

## Enumeration:
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
```
TO BE CONTINUED...
```
