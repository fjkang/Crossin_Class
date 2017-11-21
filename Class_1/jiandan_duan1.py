import urllib.request
import re

url = 'http://jandan.net/duan'

req = urllib.request.urlopen(url)
html = req.read()
html_str = html.decode('utf-8')

pattern = re.compile('</a></span><p>([\s\S]*?)<div class="jandan-vote">')
groups = pattern.findall(html_str)

for text in groups:
    text = text.replace('</div>', '')
    text = text.replace('<br />', '')
    text = text.replace('</p>', '')
    text = text.replace('<p>', '')

    print(text)
    print("=============================================")



