import requests
import pymongo
import time

client = pymongo.MongoClient()
db = client.music163
col_playlists = db.playlists
col_lyrics = db.lyrics


def get_id_detail(id):
    """根据歌单id获取歌单详细信息"""
    global headers
    print('fetching', id)
    url = 'http://music.163.com/api/playlist/detail?id={}&updateTime=-1'.format(id)
    req = requests.get(url, headers=headers)
    detail = req.json()
    # print(detail)
    print('mongo', id)
    col_playlists.update({'id': id}, {'$set': detail['result']}, upsert=True)
    print('done', id)


def get_song_lyric(id, name):
    """根据歌曲id获取歌曲的歌词"""
    global headers
    print('fetching', name)
    url = 'http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1'.format(id)
    req = requests.get(url, headers=headers)
    lyrics = req.json()
    # print(lyrics)
    lyric = lyrics['lrc']
    lyric['id'] = id
    lyric['name'] = name
    # print(lyric)
    print('mongo', name)
    col_lyrics.update({'id': id}, {'$set': lyric}, upsert=True)
    print('done', name)


headers = {
    'Cookie': 'appver=1.5.0.75771',
    'Referer': 'http://music.163.com/'
}
url = 'http://music.163.com/api/search/pc'

data = {
    's': '陈奕迅',
    'offset': 1,
    'limit': 10,
    'type': 1000,
}
req = requests.post(url, data=data, headers=headers)
data = req.json()
# print(data)

for playlist in data['result']['playlists']:
    get_id_detail(playlist['id'])
    time.sleep(2)

playlists = col_playlists.find()
for playlist in playlists:
    songs = playlist['tracks']
    for song in songs:
        get_song_lyric(song['id'], song['name'])
        time.sleep(2)