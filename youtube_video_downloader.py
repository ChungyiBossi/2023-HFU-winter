from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pytube import YouTube
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


def download_youtube(url):
    yt = YouTube(url)
    print(yt.title)           # 影片標題
    print(yt.length)          # 影片長度 ( 秒 )
    print(yt.author)          # 影片作者
    print(yt.channel_url)     # 影片作者頻道網址
    print(yt.thumbnail_url)   # 影片縮圖網址
    print(yt.views)           # 影片觀看數

    yt.streams.filter().get_highest_resolution().download(
        filename=f'{yt.title}.mp4')
    # 下載最高畫質影片，如果沒有設定 filename，則以原本影片的 title 作為檔名
    print('ok!')


if __name__ == '__main__':
    url = 'https://www.youtube.com/results?search_query=jay+chou'
    driver = webdriver.Chrome()
    driver.get(url=url)
    time.sleep(10)
    elements = driver.find_elements(By.ID, "video-title")
    for e in elements:
        href = e.get_attribute('href')
        title = e.get_attribute('title')
        if href and title and 'Official' in title:
            download_youtube(href)
            print(title)
            print(href, '\n')

    driver.quit()
