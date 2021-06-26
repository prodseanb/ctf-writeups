# POST Practice
### Challenge:
This website requires authentication, via POST. However, it seems as if someone has defaced our site. Maybe there is still some way to authenticate? http://165.227.106.113/post.php
### Solution:
When we visit the link, the output shows:
```
This site takes POST data that you have not submitted!
```
Inspecting the source code, we get random credentials.
```
<!-- username: admin | password: 71urlkufpsdnlkadsf -->
```
We can use these credentials to send a POST request. I will be using Python for this approach.<br />
The code:
```python
import requests

url = 'http://165.227.106.113/post.php'

data = {
    'username': 'admin',
    'password': '71urlkufpsdnlkadsf'
}
response = requests.post(
    url, data=data
)
print(response.content)
```
This gives us the flag:
```bash
b'<h1>flag{p0st_d4t4_4ll_d4y}</h1>'
```
Alternative method - Open up a terminal and make a POST request using curl and specify the credentials using `-d`.
```bash
curl -X POST http://165.227.106.113/post.php -d "username=admin&password=71urlkufpsdnlkadsf"
```
![POST_flag](https://user-images.githubusercontent.com/59718043/123499426-98668180-d604-11eb-89d4-ec7952413e51.png)
