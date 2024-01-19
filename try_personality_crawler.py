import pandas as pd
import csv
import time
import random
import requests
import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def save_thread_data(posts_data, pages_csv):
    result = {
        'Author': [post['Author'] for post in posts_data],
        'Thread_Title': [post['Thread_Title'] for post in posts_data],
        'Content': [post['Content'] for post in posts_data],
        'Thread_URL': [post['Thread_URL'] for post in posts_data]
    }

    df_posts = pd.DataFrame(result)
    df_posts.to_csv(pages_csv, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f"Saved data to {pages_csv}")


def crawl_thread(thread_url, driver):
    driver.get(thread_url)
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@class="MessageCard__content-inner"]'))
    )
    post_content_element = driver.find_element(
        By.XPATH, '//div[@class="bbWrapper"]')
    author_element = driver.find_element(
        By.XPATH, '//a[@class="MessageCard__user-info__name"]')
    thread_title_element = driver.find_element(
        By.XPATH, '//h1[@class="MessageCard__thread-title"]')

    post_content = post_content_element.text if post_content_element else ""
    author_name = author_element.text if author_element else ""
    thread_title = thread_title_element.text if thread_title_element else ""

    print(f"\tProcessing post from {author_name} ({thread_url})....finished!")
    result = {
        'Author': author_name,
        'Thread_Title': thread_title,  # 加入貼文標題
        'Content': " ".join(post_content.split()),
        'Thread_URL': thread_url
    }
    # print(result)
    return result


def get_chrome_driver(is_eager=True):
    options = webdriver.ChromeOptions()
    if is_eager:
        options.page_load_strategy = 'eager'
    # options.add_argument('--headless')
    driver = webdriver.Chrome(
        options=options
    )
    return driver


def get_total_page_number(forum_url):
    driver = get_chrome_driver()
    # 初始頁面
    driver.get(forum_url)
    print('Get forum web page.')
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'structItem-title'))
    )

    # 找到qid為"page-nav-other-page"的元素
    # page_nav_element = soup.select_one('[qid="page-nav-other-page"]')
    page_nav_element = driver.find_element(
        By.XPATH, '//*[@qid="page-nav-other-page"]')

    # 從中獲取頁數
    total_pages = int(page_nav_element.text)
    print("Total pages: ", total_pages)

    driver.quit()

    return total_pages


def collect_thread_urls(base_url, forum_name, thread_limit):
    thread_urls = list()
    total_pages = get_total_page_number(base_forum_url)
    with get_chrome_driver() as driver:
        for page in range(1, total_pages + 1):
            # Stop condition
            if thread_limit < len(thread_urls):
                print('Exceed thread limit, collection complete')
                break
            print(f'{"=" * 10} Page {page} start {"=" * 10}')
            # 動態生成網址
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}page-{page}?sorting=latest-activity"
            driver.get(url)
            time.sleep(10)
            # WebDriverWait(driver, 30).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, '//a[@class=" thread-title--gtm"]'))
            # )
            thread_links_elements = driver.find_elements(
                By.XPATH, '//a[@class=" thread-title--gtm"]')

            # 模擬滾動以加載更多帖子，這部分可視情況選擇是否需要
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            # To solve bug: Message: stale element reference: stale element not found
            # need to store thread links to prevent bug above
            links = list()
            for elements in thread_links_elements:
                link = elements.get_attribute('href')
                links.append(link)

            thread_urls += links
            time.sleep(random.randint(1, 5))
            print(f'Collect {len(thread_urls)} threads.')
            print(f'{"=" * 10} Page {page} end {"=" * 10}')
        driver.quit()

    threads = {
        'thread_url': thread_urls
    }
    pd.DataFrame(threads).to_csv(f'data_personality/{forum_name}_threads_url.csv',
                                 index=False, quoting=csv.QUOTE_NONNUMERIC)

    return thread_urls


def crawl_personlitycafe_forum(thread_urls, forum_name):
    posts_data = list()
    with get_chrome_driver() as driver:
        for i, thread_url in enumerate(thread_urls):
            try:
                time.sleep(random.randint(1, 5))  # random sleep
                post_content = crawl_thread(
                    thread_url, driver)  # get thread content
                posts_data.append(post_content)  # 處理該作者的貼文內容
            except TimeoutException:
                print(
                    f"TimeoutException: Timed out on thread {i + 1}. Skipping...")
                time.sleep(30)
                continue
            except Exception as e:
                print("Something wrong:", e)
                print(f"Save log and current index.{i}")
                with open(f'checkpoint_{time.asctime()}.json', 'w') as cp:
                    checkpoint = {
                        'forum_name': forum_name,
                        'current_index': i
                    }
                    cp.write(json.dumps(checkpoint))

            time.sleep(random.randint(1, 5))

            if i % 200 == 0:
                save_thread_data(
                    posts_data, f'data_personality/{forum_name}_{i}.csv')
                posts_data = list()
                driver.quit()
                driver = get_chrome_driver()
        driver.quit()
    # 檢查爬取到的作者數量是否足夠
    print(f'Finish this forum: {forum_name}')
    return posts_data


# 設定論壇基本網址
base_forum_urls = [
    "https://www.personalitycafe.com/forums/istp-forum-the-mechanics.9/",
    # "https://www.persoalitycafe.com/forums/enfj-forum-the-givers.17/",
    "https://www.personalitycafe.com/forums/enfp-forum-the-inspirers.19/",
    "https://www.personalitycafe.com/forums/entj-forum-the-executives.13/",
    "https://www.personalitycafe.com/forums/entp-forum-the-visionaries.15/",
    "https://www.personalitycafe.com/forums/esfj-forum-the-caregivers.8/",
    "https://www.personalitycafe.com/forums/esfp-forum-the-performers.11/",
    "https://www.personalitycafe.com/forums/estj-forum-the-guardians.6/",
    "https://www.personalitycafe.com/forums/estp-forum-the-doers.10/",
    "https://www.personalitycafe.com/forums/infj-forum-the-protectors.18/",
    "https://www.personalitycafe.com/forums/infp-forum-the-idealists.20/",
    "https://www.personalitycafe.com/forums/intj-forum-the-scientists.14/",
    "https://www.personalitycafe.com/forums/intp-forum-the-thinkers.16/",
    "https://www.personalitycafe.com/forums/isfj-forum-the-nurturers.7/",
    "https://www.personalitycafe.com/forums/isfp-forum-the-artists.12/",
    "https://www.personalitycafe.com/forums/istj-forum-the-duty-fulfillers.5/",
]
# base_forum_url = "https://www.personalitycafe.com/forums/istp-forum-the-mechanics.9/"

# PART 1:設定要爬取的作者數目，取得所有的thread urls 並存起來
# for base_forum_url in base_forum_urls:
#     # 設定輸出檔案的路徑
#     forum_name = base_forum_url.split('/')[-2]

#     print('Forum url: ', base_forum_url)
#     print('Forum name: ', forum_name)

#     url_collection_filename = f'data_personality/{forum_name}_threads_url.csv'
#     if os.path.exists(url_collection_filename):
#         print("Thread url collections find.")
#         thread_urls = pd.read_csv(url_collection_filename)['thread_url']
#     else:
#         try:
#             # Get Thread Url
#             print("Start Collecting")
#             thread_urls = collect_thread_urls(base_forum_url, forum_name, 1000)
#         except Exception as e:
#             print("Something Wrong: ", e)
#             print("Skipping this forum.")
#             continue

# PART 2: 爬取內容
# 設定要爬取的作者數目
for base_forum_url in base_forum_urls:

    # 設定輸出檔案的路徑
    forum_name = base_forum_url.split('/')[-2]
    print('Forum url: ', base_forum_url)
    print('Forum name: ', forum_name)
    # 爬取資料
    url_collection_filename = f'data_personality/{forum_name}_threads_url.csv'
    if os.path.exists(url_collection_filename):
        print("Thread url collections find.")
        thread_urls = pd.read_csv(url_collection_filename)['thread_url']
        try:
            all_posts_data = crawl_personlitycafe_forum(
                thread_urls, forum_name=forum_name)
        except Exception as e:
            print("Something Wrong: ", e)
            print("Skipping this forum.")
            continue
