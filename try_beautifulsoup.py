from bs4 import BeautifulSoup
import requests
from pprint import pprint


def find_news(soup, is_show_sample=False):
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
        pprint(list_of_news_info[0])

    return list_of_news_info


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
    result = find_news(soup, is_show_sample=True)
