import time
import random
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


query = '林俊傑'
url = f'https://www.youtube.com/results?search_query={query}'
# Use Selenium Chrome driver
driver = webdriver.Chrome()
driver.fullscreen_window()  # 才有onfocus()
driver.get(url)
# Get scroll height
js_getScrollHeight = "return document.documentElement.scrollHeight"
xpath_noResultFound = "//yt-formatted-string[@class='style-scope ytd-message-renderer'][text()='沒有其他結果']"

current_height = 0
target_height = driver.execute_script(js_getScrollHeight)
retry_count = 0
while True:
    if current_height == target_height:
        try:
            # 等待搜尋底部：<yt-formatted-string id="message" class="style-scope ytd-message-renderer">沒有其他結果</yt-formatted-string>
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath_noResultFound))
            )
            print("Scroll finished. ")
            break
        except TimeoutException:
            retry_count += 1
            print(f"Scroll not fininsh. - {retry_count}")
            driver.execute_script("window.onfocus();")  # 保持模擬瀏覽器聚焦在windows上
            if retry_count > 25:
                print("為了避免永久執行，終止滾輪程式")
                break
    else:
        retry_count = 0
        current_height = target_height
        driver.execute_script(
            f"window.scrollTo(0, {current_height});")
        time.sleep(random.randint(1, 3))

    target_height = driver.execute_script(js_getScrollHeight)

# 找到當前目錄所有的a，而且attribute class是'video-title'的
selenium_elements = driver.find_elements(By.XPATH, "//a[@id='video-title']")
print('selenium_elements: ', len(selenium_elements))
