from bs4 import BeautifulSoup
with open('test2.txt', 'r', encoding='utf-8') as f:
    code = f.read()

soup =BeautifulSoup(code,'html.parser')

print(soup.find_all(class_='col-sm-4'))