import requests
import re
import json
from pprint import pprint

url = 'https://www.youtube.com/results?search_query=%E5%91%A8%E6%9D%B0%E5%80%AB'
r = requests.get(url)
pattern = re.compile(r'var\s+ytInitialData\s*=\s*({.*?});')
data = re.findall(pattern=pattern, string=r.content.decode('utf-8'))
data = json.loads(data[0])


# primaryContents & secondaryContents
for key in data['contents']['twoColumnSearchResultsRenderer']:
    print(key)

print('='*50)

# primaryContents
primary_content_urls = list()
for content in data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']:
    if 'itemSectionRenderer' in content:
        for i_content in content['itemSectionRenderer']['contents']:
            if 'videoRenderer' in i_content:
                url = 'https://youtube.com' + \
                    i_content['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
                # print(url)
                primary_content_urls.append(url)


# secondaryContents
secondary_content_urls = list()
secondary_content = \
    data['contents']['twoColumnSearchResultsRenderer']['secondaryContents'][
        'secondarySearchContainerRenderer']['contents'][0]['universalWatchCardRenderer']
secondary_content_cards = \
    secondary_content['sections'][0]["watchCardSectionSequenceRenderer"]['lists'][0]['verticalWatchCardListRenderer']['items']
for card in secondary_content_cards:
    card_content = card["watchCardCompactVideoRenderer"]
    card_title = card_content['title']['simpleText']
    url = 'https://youtube.com' + \
        card_content['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
    secondary_content_urls.append(url)


pprint(len(primary_content_urls))
pprint(len(secondary_content_urls))
