from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

url = "https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
driver.get(url=url)
time.sleep(3)
print(len(driver.page_source))

a_elements = driver.find_elements(By.XPATH, '//a[@class="WwrzSb"]')
print(len(a_elements))
# for a_element in a_elements:
#     print(a_element.get_attribute('href'))


driver.quit()
