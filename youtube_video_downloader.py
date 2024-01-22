from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
from pytube import YouTube
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


def correct_filename(ouput_folder_name='yt_videos'):
    for file_name in os.listdir(ouput_folder_name):
        if file_name.endswith('.mp3"'):
            wrong_file_name = f'{ouput_folder_name}/{file_name}'
            new_filename = file_name.replace('.mp3"', '.mp3')
            new_filename = f"{ouput_folder_name}/{new_filename}"
            if os.path.exists(new_filename):
                print(f"新的檔案名 '{new_filename}' 已存在，清除此檔案。")
                os.remove(wrong_file_name)
            else:
                # 重新命名檔案
                os.rename(wrong_file_name, new_filename)
                print(f"檔案已成功重新命名為 '{new_filename}'。")


def download_youtube(url, max_length=10*60, show_video_info=False, download_video=False):
    yt = YouTube(url)
    if show_video_info:
        print(yt.title)           # 影片標題
        print(yt.length)          # 影片長度 ( 秒 )
        print(yt.author)          # 影片作者
        print(yt.channel_url)     # 影片作者頻道網址
        print(yt.thumbnail_url)   # 影片縮圖網址
        print(yt.views)           # 影片觀看數

    if yt.length <= max_length:
        file_name = yt.title.replace("/", " ")
        if download_video:
            yt.streams.filter().get_highest_resolution().download(
                filename=f'yt_videos/{file_name}.mp4')
        else:
            yt.streams.filter().get_audio_only().download(
                filename=f'yt_videos/{file_name}.mp3'
            )
    # 下載最高畫質影片，如果沒有設定 filename，則以原本影片的 title 作為檔名
    print('ok!')


if __name__ == '__main__':
    singer_list = [
        # '茄子蛋',
        # '張學友',
        # '陳昇',
        # '伍佰',
        # '陳奕迅',
        # '劉德華',
        # '林志炫',
        # '張雨生',
        # '王傑',
        # '楊乃文',
        # '葉歡',
        # '林隆璇',
        # '那英',
        # '李聖傑',
        # '周華健',
        # '梁靜茹',
        # '曹格',
        # '張信哲',
        # '張宇',
        # '萬芳',
        # '黃品源',
        # '小安',
        # '任賢齊',
        # '辛曉琪',
        # '梁詠琪',
        # '李宗聖',
        # 'Beyond',
        '王菲'
    ]

    correct_filename()

    driver = webdriver.Chrome()
    for singer in singer_list:
        url = f'https://www.youtube.com/results?search_query={singer}'
        driver.get(url=url)
        time.sleep(15)

        max_retry = 5
        for times in range(max_retry):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            elements = driver.find_elements(
                By.XPATH, '//a[@id="video-title"]')
            if len(elements) > 20:
                break
            else:
                print(f'Waiting {url} completed loaded...{times}')
                time.sleep(5)

        print(f'Done, search:{singer}, {len(elements)} result find.')
        for e in elements:
            href = e.get_attribute('href')
            title = e.get_attribute('title')
            if href and title and ('official' in title.lower() or '官方' in title.lower() or 'music video' in title.lower()):
                download_youtube(
                    url=href,
                    max_length=10*60,
                    show_video_info=False,
                    download_video=False
                )
                print(title)
                print(href, '\n')
                time.sleep(random.randint(5, 10))
            else:
                print(f'標題不符合: {title}')
        time.sleep(60)
    driver.quit()

    # download only one video with yt url
    # download_youtube('https://www.youtube.com/watch?v=EWpIAHLvrf4')
