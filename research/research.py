import requests

url = 'http://127.0.0.1:8000/projects/projects/1/confirm/'

response = requests.post(url)

print(response.content)


import requests
url = 'http://127.0.0.1:8000/projects/projects/1/'

response = requests.get(url)

print(response.json())