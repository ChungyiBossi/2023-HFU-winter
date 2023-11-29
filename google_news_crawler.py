from bs4 import BeautifulSoup
import requests
from pprint import pprint


def find_news(soup, base_href, is_show_sample=False):
    # 期望的資料格式
    list_of_news_info = list()

    # 找新聞資料的超連結element
    a_elements = soup.find_all('a', {'class': 'WwrzSb'})
    for element in a_elements:
        if 'href' in element.attrs:
            href_element = element  # 先找到超連結的節點(element)
            grandpa_element = element.find_parents(
                'article')[0]  # 藉由超連結結點，找到共同的父節點
            title_element = grandpa_element.find_all(
                'h4')[0]  # 藉由父節點，找到title的子節點
            media_name_element = grandpa_element.find_all(
                'div', {'class': 'vr1PYe'})[0]  # 媒體是誰

            if href_element and title_element:
                news_info = {
                    'news_title': title_element.string,
                    'href': base_href + element['href'][2:],
                    'media': media_name_element.string
                }
                list_of_news_info.append(news_info)

            # Debug log
            # print(element['class'], base_href + element['href'][2:])
            # print(grandpa_element.name)
            # print(title_element.name)
            # print(media_name_element.string)
            # print()
    if is_show_sample:
        print('Total news number:', len(list_of_news_info))
        pprint(list_of_news_info)

    return list_of_news_info


def generate_web_page(list_of_news_info):
    news_articles = ""
    for news_info in list_of_news_info:
        news_title = news_info['news_title']
        media_name = news_info['media']
        href = news_info['href']
        article = f"""
            <article>
                <h3><a href=\"{href}\">{news_title}</a></h3>
                <br/>
                <media>{media_name}</media>
            </article>
        """

        news_articles = news_articles + article

    generate_html_page = """ 
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>新聞網</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }

            header {
                background-color: #333;
                color: #fff;
                text-align: center;
                padding: 1em;
            }

            main {
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            article {
                margin-bottom: 20px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 20px;
            }

            h2 {
                color: #333;
            }

            p {
                color: #666;
            }

            time {
                color: #999;
            }

            footer {
                text-align: center;
                padding: 1em;
                background-color: #333;
                color: #fff;
            }
        </style>
    </head>

    <body>

        <header>
            <h1>新聞網</h1>
        </header>

        <main>
    """ + news_articles + """
        </main>
        <footer>
            &copy; 2023 新聞網. All rights reserved.
        </footer>
    </body>
    </html>"""
    return generate_html_page


if __name__ == '__main__':
    # 取得網頁回覆
    url = 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JYcG9MVlJYS0FBUAE?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
    r = requests.get(url)

    # 確定 r 是什麼東西？ 是 html 才走下一步
    small_soup = BeautifulSoup(r.content[:200], 'html.parser')
    base_href = small_soup.base['href']

    # 把 HTML 轉化成 “湯”
    soup = BeautifulSoup(r.content, 'html.parser')
    # 看一下DOM樹
    result = find_news(soup, base_href=base_href, is_show_sample=True)

    # 生成 news html
    generated_html = generate_web_page(result)

    # 寫入到檔案內
    # 開啟一個“news_web_page.html”, 並允許可以寫入, 代稱page
    # 生命週期在這個"with"完成後結束，並寫入你生成的html文字
    with open("news_web_page.html", "w") as page:
        page.write(generated_html)
