from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

EMAIL = 'GMAIL'
PASSWORD = "PASSWORD"

# driver = webdriver.Chrome() # selenium webdriver 會被google search 擋住
driver = uc.Chrome()
# google login url
url = 'https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dgoogle%2B%25E7%2599%25BB%25E5%2585%25A5%26rlz%3D1C5CHFA_enTW969TW969%26oq%3Dgoogle%2B%25E7%2599%25BB%25E5%2585%25A5%26gs_lcrp%3DEgZjaHJvbWUyBggAEEUYOTIGCAEQRRhA0gEIMzg4NmowajeoAgCwAgA%26sourceid%3Dchrome%26ie%3DUTF-8&ec=GAZAAQ&hl=zh-TW&ifkv=ASKXGp3QryzAjE0knNfUu47LhOa7xamGWPzdQyIIFxDn6N_DP-3gX4AX1aOH7NpEH8LoWhyn-25R&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S486807008%3A1702536821223868&theme=glif'
driver.get(url)

driver.find_element(By.ID, "identifierId").send_keys(EMAIL)
time.sleep(5)
driver.find_element(
    By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]').click()
time.sleep(5)
driver.find_element(By.XPATH, '//input[@name="Passwd"]').send_keys(PASSWORD)
driver.find_element(
    By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]').click()
time.sleep(50)
