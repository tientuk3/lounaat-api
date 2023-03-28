import requests

url = 'https://www.lounaat.info/00380-helsinki'

try:
    response = requests.get(url)
    with open('example.html', 'w') as file:
        file.write(response.text)
    print("ok")
except Exception as e:

    print("fail")
    print(e)