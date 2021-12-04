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
Found a site with input fields that could be potential entry points.
<br/><br/>
![Screenshot at 2021-12-03 21-38-40](https://user-images.githubusercontent.com/59718043/144700412-347e85cf-7ea9-498c-807e-81c702acb9a0.png)
<br/><br/>
Another potential vulnerability: `Werkzeug/0.16.1 Python/3.8.5`.
```
TO BE CONTINUED
```
