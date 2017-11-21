import requests
from pyquery import PyQuery as pq
import pymongo

client = pymongo.MongoClient()
db = client.nuomi
col_citycode = db.citycode
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
}
url = 'https://mdianying.baidu.com/city/choose?sfrom=wise_shoubai&from=webapp&sub_channel=&source=&c=259&cc=259&kehuduan='

html = requests.get(url, headers=headers)
doc = pq(html.text)
a = doc('a.city-item')
for i in range(len(a)):
    cityname = a.eq(i).text()
    citycode = a.eq(i).attr('data-citycode')
    print('collect', cityname)
    col_citycode.update({'citycode': citycode}, {'$set': {'cityname': cityname, 'citycode': citycode}}, upsert=True)
    print('saved')
