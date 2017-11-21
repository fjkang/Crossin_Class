import time

date = '2017-11-17'
timeArray = time.strptime(date, "%Y-%m-%d")

timestamp = int(time.mktime(timeArray))
print(timestamp)