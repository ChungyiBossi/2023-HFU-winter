from chat_downloader import ChatDownloader

url = 'https://www.youtube.com/watch?v=5H-d0CE7_CY'
chat = ChatDownloader().get_chat(url)       # create a generator
for message in chat:                        # iterate over messages
    chat.print_formatted(message)           # print the formatted message
