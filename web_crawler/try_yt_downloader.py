import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytube import YouTube
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


url = 'https://www.youtube.com/results?search_query=%E5%91%A8%E6%9D%B0%E5%80%AB'

# 要找到所有的 <a class='video-title' href='....'/>，
# 其中的href是我們要的影片連結，用來丟給pytube

# # (x) Solution 1: requests 取回網頁內容，再丟給漂亮湯parse成DOM tree
# r = requests.get(url)
# soup = BeautifulSoup(r.content, 'html.parser')
# elements = soup.find_all(name='a', attrs={'id': 'video-title'})
# print('bs4 elements: ', len(elements))

# Solution 2: use Selenium Chrome driver
cService = webdriver.ChromeService(
    executable_path=r'/Users/chungilin/2023_hfu_winter/chromedriver')
driver = webdriver.Chrome(service=cService)
# driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
driver.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);"
)
time.sleep(10)
# 找到當前目錄所有的a，而且attribute class是'video-title'的
selenium_elements = driver.find_elements(By.XPATH, "//a[@id='video-title']")
print('selenium_elements: ', len(selenium_elements))

for s_element in selenium_elements:
    href = s_element.get_attribute('href')
    title = s_element.get_attribute('title')
    if href and title:
        if 'official' in title.lower():
            print("link:", href)
            yt = YouTube(href)
            # print(yt.title)           # 影片標題
            # print(yt.length)          # 影片長度 ( 秒 )
            # print(yt.author)          # 影片作者
            # print(yt.channel_url)     # 影片作者頻道網址
            # print(yt.thumbnail_url)   # 影片縮圖網址
            # print(yt.views)           # 影片觀看數
            file_name = yt.title.replace('/', '')
            # yt.streams.\
            #     filter().\
            #     get_highest_resolution().\
            #     download(filename=f'test_yt_save/{file_name}.mp4')
            yt.streams.\
                filter().\
                get_audio_only().\
                download(filename=f'yt_save/{file_name}.mp3')
