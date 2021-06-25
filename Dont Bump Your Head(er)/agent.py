import requests

url = 'http://165.227.106.113/header.php'

user_agent = 'Sup3rS3cr3tAg3nt'
headers = {'User-Agent': f'{user_agent}','Referer':'awesomesauce.com'}
response = requests.get(url, headers=headers)
print(response.content)