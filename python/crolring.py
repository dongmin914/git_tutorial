from cgitb import html
import requests
from bs4 import BeautifulSoup

htmls = requests.get('https://naver.com/')
# print(htmls.text)

bs = BeautifulSoup(htmls.content, 'html.parser')

print(bs.h1)

title = bs.find('title')

bs.find_all(attrs={})


 