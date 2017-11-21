import requests
import csv


max_behot_time = [1504060792]
csv_file = r'D:\toutiao.csv'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
           }


def get_data(url):
    global max_behot_time
    item_lst = []
    req = requests.get(url, headers=headers)
    json = req.json()
    data = json['data']
    max_behot_time.append(json['next']['max_behot_time'])
    for item in data:
        lst = []
        try:
            lst.append(item['title'])
            lst.append(item['abstract'])
            lst.append(item['comments_count'])
            item_lst.append(lst)
        except Exception as e:
            # print(e)
            continue
    return item_lst


def save_to_csv(data_lst, csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['标题', '概述', '评论数'])
        for item in data_lst:
            writer.writerow(item)


def main():
    data_lst = []
    url_base = "https://www.toutiao.com/api/pc/feed/?category=news_sports&utm_source=toutiao&widen=1&max_behot_time="
    url = url_base + str(max_behot_time.pop())
    for i in range(5):
        item_lst = get_data(url)
        data_lst.extend(item_lst)
    print(data_lst)
    save_to_csv(data_lst, csv_file)


if __name__ == '__main__':
    main()