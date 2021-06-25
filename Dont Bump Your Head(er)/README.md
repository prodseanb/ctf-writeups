# Don't Bump Your Head(er)
### Challenge:
Try to bypass my security measure on this site! http://165.227.106.113/header.php
### Solution:
For this challenge, I decided to take the Pythonic approach.
When we visit the link, the output shows:
```
Sorry, it seems as if your user agent is not correct, in order to access this website. The one you supplied is: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0 
```
Spoofing the user agent and modifying the request headers would be an easy job for Burp but I decided to dissect this CTF in Python.<br />
 I had a hunch that `Sup3rS3cr3tAg3nt` is our hint. I decided to switch the user agent to this value.
 ```python
 import requests
 
 url = 'http://165.227.106.113/header.php'
 user_agent = 'Sup3rS3cr3tAg3nt'
 # Modify headers
 headers = {'User-Agent': f'{user_agent}'}
 response = requests.get(url, headers=headers)
 print(response.content)
 ```
 Output:
 ```bash
 b'Sorry, it seems as if you did not just come from the site, "awesomesauce.com".\n<!-- Sup3rS3cr3tAg3nt  -->\n'
 ```
 It turns out that we need `awesomesauce.com` as a referer in our headers. We should modify our code to add this to the header.
 ```python
 headers = {'User-Agent': f'{user_agent}','Referer':'awesomesauce.com'}
 ```
 Output:
 ```bash
 b'Here is your flag: flag{did_this_m3ss_with_y0ur_h34d}\n<!-- Sup3rS3cr3tAg3nt  -->\n'
 ```
 ![header_flag](https://user-images.githubusercontent.com/59718043/123368959-c7202180-d54a-11eb-92f1-56311b0267e3.png)
