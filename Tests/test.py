import requests

#response = requests.request('GET', 'http://www.massmarketing.se')

response = requests.post(
    'http://duckduckgo.com',
    data={'q': 'tkinter', 'ko': '-2', 'kz': '-1'})

print(response)