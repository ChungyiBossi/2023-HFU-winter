from chat_downloader import ChatDownloader
import json
headers = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
url = 'https://www.youtube.com/watch?v=2bIRjTiAHms'


outputs = {
    'original_url':  url,
    'chatroom': list()
}
chat = ChatDownloader(
    # headers=headers
).get_chat(url)       # create a generator
for message in chat:                        # iterate over messages
    chat.print_formatted(message)           # print the formatted message
    outputs['chatroom'].append(message)

with open('2024大選總統候選人辯論會.json', 'w') as json_file:
    data = json.dump(outputs, json_file)
