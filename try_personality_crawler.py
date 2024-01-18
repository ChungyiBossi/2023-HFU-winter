import pandas as pd
import csv
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def save_data(posts_data, pages_csv):
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


def crawl_personlitycafe_forum(base_url, author_limit, output_folder='data_personality', forum_name="istp_posts_data.csv"):
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(
        options=options
    )

    authors_set = set()
    posts_data = []
    # 初始頁面
    url = base_url
    driver.get(url)
    print('Get forum web page.')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'structItem-title'))
    )

    # 找到qid為"page-nav-other-page"的元素
    # page_nav_element = soup.select_one('[qid="page-nav-other-page"]')
    page_nav_element = driver.find_element(
        By.XPATH, '//*[@qid="page-nav-other-page"]')

    # 從中獲取頁數
    total_pages = int(page_nav_element.text)
    print("Total pages: ", total_pages)

    for page in range(1, total_pages + 1):
        # for page in range(1, 3):
        # 動態生成網址
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}page-{page}?sorting=latest-activity"

        print(f'{"=" * 10} Page {page} start {"=" * 10}')
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[@class=" thread-title--gtm"]'))
        )
        thread_links_elements = driver.find_elements(
            By.XPATH, '//a[@class=" thread-title--gtm"]')

        # To solve bug: Message: stale element reference: stale element not found
        # need to store thread links to prevent bug above
        links = list()
        for elements in thread_links_elements:
            link = elements.get_attribute('href')
            links.append(link)

        print(f'{len(links)} threads find')
        for i, thread_url in enumerate(links):
            try:
                # random sleep
                time.sleep(random.randint(1, 5))
                # get thread content
                post_content = crawl_thread(thread_url, driver)
                # 檢查是否已經爬取過該作者的貼文
                if post_content['Author'] not in authors_set:
                    authors_set.add(post_content['Author'])

                    # 處理該作者的貼文內容
                    posts_data.append(post_content)

                # 如果已經達到指定作者數目，則退出迴圈
                if len(authors_set) >= author_limit:
                    break
            except TimeoutException:
                print(
                    f"TimeoutException: Timed out on thread {i + 1}. Skipping...")
                pass
            time.sleep(random.randint(1, 5))

        # 如果已經達到指定作者數目，則退出迴圈
        if len(authors_set) >= author_limit:
            print(
                f'{len(authors_set)} meet the author limit, finishing the crawling....')
            break
        else:
            print(f'Find author {len(authors_set)}, continue')
        # 模擬滾動以加載更多帖子，這部分可視情況選擇是否需要
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        print(f'{"=" * 10} Page {page} end {"=" * 10}')

        if page % 5:
            pages_csv = f"{output_folder}/{forum_name}_{page-4}-{page}.csv"
            save_data(posts_data=posts_data, pages_csv=pages_csv)
            print(f"Saved data to {forum_name}")
            posts_data = list()

        pages_csv = f"{output_folder}/{forum_name}_{page-5*(page//5)}-{page}.csv"
        save_data(posts_data=posts_data, pages_csv=forum_name)
        print(f"Saved data to {forum_name}")

    driver.quit()
    # 檢查爬取到的作者數量是否足夠
    if len(authors_set) < author_limit:
        print(
            f"Warning: Only crawled {len(authors_set)} unique authors, which is less than the required {author_limit}. The data may not be sufficient.")

    return posts_data


# 設定論壇基本網址
base_forum_urls = [
    "https://www.personalitycafe.com/forums/istp-forum-the-mechanics.9/",
    "https://www.persoalitycafe.com/forums/enfj-forum-the-givers.17/",
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

# 設定要爬取的作者數目
author_limit = 500 * len(base_forum_urls)
for base_forum_url in base_forum_urls:
    # 設定輸出檔案的路徑
    forum_name = base_forum_url.split('/')[-2]

    print('Forum url: ', base_forum_url)
    print('Forum name: ', forum_name)
    # 爬取資料
    all_posts_data = crawl_personlitycafe_forum(
        base_forum_url, author_limit, forum_name=forum_name)

    # 將所有的資料轉換成 DataFrame
    df_all_posts = pd.DataFrame(all_posts_data)
