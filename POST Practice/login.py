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