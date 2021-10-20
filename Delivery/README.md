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

Edited `/etc/hosts` and included delivery.htb and helpdesk.delivery.htb.
![Screenshot_2021-10-19_22_26_18](https://user-images.githubusercontent.com/59718043/138018087-0432a42a-fae6-41c6-a1ff-b8882a260eb7.png)
Opened a ticket through this portal, used the `Check Ticket Status` functionality to login to view ticket status.
<br/><br/>
Then I went to delivery.htb:8065 to create a new account, checked back on the ticket status page and saw a verification link. This link took me to a login page.
Used the credentials to log in, this brought me to the MatterMost server.
<br/><br/>
![Screenshot_2021-10-19_23_27_16](https://user-images.githubusercontent.com/59718043/138023512-752dcf27-0df6-4f76-a1f0-29c70fb62b6a.png)
```
TO BE CONTINUED.
```
