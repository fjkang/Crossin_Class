import json
from collections import Counter
import pymongo

client = pymongo.MongoClient()
db = client.sixsix
col_proxy = db.proxies

data = col_proxy.find()
port = []
for proxy in data:
    port.append(proxy['port'])

port_count = Counter(port)
top_10 = port_count.most_common(10)
most_count = 0
port_name = []
port_num = []
for i in top_10:
    most_count += i[1]
    port_name.append(i[0])
    port_num.append(i[1])
port_name.append('其他')
other_count = len(port)-most_count
port_num.append(other_count)
print(port_name)
print(port_num)

