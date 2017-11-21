import requests

proxies = {
    'https': 'https://112.74.94.142:3128'
}
# url = 'https://ddns.oray.com/checkip'
# check = requests.get(url, proxies=proxies, timeout=20)
# print(check.text)
url = 'https://lab.crossincode.com/proxy/get/?num=5'
req = requests.get(url, proxies=proxies, timeout=20)
print(req.json())


