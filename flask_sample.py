import random
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template
from google_news_crawler import find_news


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<name>/")
def hello(name):
    return f"Hello, <script>alert('{name}')</script>!"


@app.route('/news/')
def inject_news_to_template():
    rand_integer = random.randint(1, 100)

    # 取得網頁回覆
    url = 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JYcG9MVlJYS0FBUAE?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
    r = requests.get(url)
    small_soup = BeautifulSoup(r.content[:200], 'html.parser')
    base_href = small_soup.base['href']
    soup = BeautifulSoup(r.content, 'html.parser')
    result = find_news(soup, base_href=base_href, is_show_sample=True)

    # rand_integer是後端python用的變數名字，integer是稍後在前端模板用的變數名
    return render_template(
        'news_web_page.html',
        integer=rand_integer,
        news_info=result   # **kwargs
    )
