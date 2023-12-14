import requests
from bs4 import BeautifulSoup

url = "https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
a_elements = soup.find_all('a', {'class': 'WwrzSb'})

print(len(a_elements))
