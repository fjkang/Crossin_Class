import time

import requests
import pymongo


client = pymongo.MongoClient()
db = client.douban
collections = db.movies
col_casts = db.casts
proxies = {
    'https': 'https://112.74.94.142:3128'
}

def get_cast(id):
    global proxies
    if not id:
        return
    print('fetching', id)
    try:
        casts_id = id
        url = 'https://api.douban.com/v2/movie/celebrity/' + str(casts_id)
        print(proxies)
        req = requests.get(url, proxies=proxies, timeout=20)
        data = req.json()
        print('collecting', id)
        col_casts.update_one({'id': casts_id}, {'$set': data}, upsert=True)
        print('done', id)
    except Exception as e:
        print(e, id)


for movie in collections.find():
    casts = movie['casts']
    print(movie['title'], ':')
    for cast in casts:
        name, id = cast['name'], cast['id']
        print(name, ':', id)
        get_cast(id)
        time.sleep(5)