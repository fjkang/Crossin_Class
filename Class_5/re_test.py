import re

url = 'https://www.s.cn/originals-brand.html'
pattern = "https://www.s.cn/(\w+)-brand.html"
brand = re.match(pattern, url)
brand = brand.group(1)
