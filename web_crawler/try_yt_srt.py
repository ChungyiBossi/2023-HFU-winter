from pytube import YouTube
url = 'https://www.youtube.com/watch?v=5H-d0CE7_CY'
yt = YouTube(url)
yt.bypass_age_gate()  # 忽略年齡限制，有BUG，解法在:https://github.com/pytube/pytube/issues/1712
print(yt.captions)                                 # 取得所有語系
caption = yt.captions.get_by_language_code('zh-TW')   # 取得英文語系

xml = caption.xml_captions if caption else None

print(xml)
