import requests
from bs4 import BeautifulSoup

url = 'https://www.personalitycafe.com/threads/enfj-video.893450/'
# url = 'https://www.youtube.com/watch?v=Evr3xVwhyPc&t=13246s'


cookie = '''guest_hash=44af75870bb9d22e5f6b43a223f933aa01c5121a977d7b9bc85ecec2cdafa222; xf_csrf=UfrhZ-c-zU0b6MH3; release_hash=285436d7; _gid=GA1.2.2048662631.1705941500; _pbjs_userid_consent_data=3524755945110770; _sharedid=49308f89-839a-46f4-9014-db9c89503107; g_state={"i_p":1705948713320,"i_l":1}; isInTestGroup_vs-peb2=1; experiment_vs-peb2=green; isInTestGroup_vs-pe-3=1; experiment_vs-pe-3=green; isInTestGroup_primisRightRailABExp=1; experiment_primisRightRailABExp=original; lux_uid=170594494302909759; _gat_UA-37540213-14=1; _ga_L2F1D7LD2Q=GS1.1.1705944942.3.1.1705944943.0.0.0; _ga=GA1.1.491812138.1705640791; xf_page_view_counter=7; cto_bundle=cKsbJF91bmdpQUtvUzBNclI5VDdaZmlRMlVNOUFHWnZqRVQ0QkRHVjhSVGdJaGoyZFRTQXFBY2NVa1FBTzdVJTJCWU4wN0dLRFdaa0ZCMW5QciUyRjZZTnRqYkpPVWVmMWt4eWhYR0ViOG41UzJWcFhnQmtUandkaWlVeVN0JTJCbW55bTE2N0xTV1l4ZVN6a1BxeTB6NmJQRHhjVmh4MHJEVDFicmlaYSUyRkl4NDlaZVZBNmFwMCUzRA; cto_bidid=WoFuVV9PbFJYRXZxJTJCaHRINHFYVmhIOWV1cTlVM1VvQk1hNUtZY2Q0N1ZnYUt5S3h1SVB6UUFraDBEMzc3YkJUTE1CN3NYbWFVJTJCTEpZMUVKVmFRZFQlMkIwT1c4VCUyQmJ4RDNQbnFkQkVtRjZmaFVWd1BYUEx0clAlMkZTbkZsMWl2SWJlR3lkRW8'''
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'accept': 'text/html; charset=utf-8,*/*,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'text/html; charset=utf-8',
    'cookie': cookie
}

r = requests.get(
    url,
    headers=headers
)
r.encoding = 'utf8'
# soup = BeautifulSoup(r.content)
# elements = soup.find_all('div', attrs={'class': "bbWrapper"})
# print(elements)

print(r.text, r.status_code)
