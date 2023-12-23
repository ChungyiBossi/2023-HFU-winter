from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import os


def start_chrome_with_profile(user_data_dir, profile_dir):
    # 利用本地的Profile登入google
    # workaround: 必須把profile複製到其他的檔案夾才可用，原因是DevToolActivatePool會因沒有headless參數而被刪除，導致找不到session
    # reference: https://stackoverflow.com/questions/77456929/how-to-use-google-chrome-user-in-selenium-webdriver-python-updated
    user_data_dir_arg = f"--user-data-dir={user_data_dir}"
    profile_dir_arg = f"--profile-directory={profile_dir}"
    options = webdriver.ChromeOptions()
    options.add_argument(user_data_dir_arg)
    options.add_argument(profile_dir_arg)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    return driver


def start_chrome_with_semi_auto_login(email, password):
    chrome_options = uc.ChromeOptions()
    driver = uc.Chrome(chrome_options=chrome_options)

    # google login url
    url = 'https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dgoogle%2B%25E7%2599%25BB%25E5%2585%25A5%26rlz%3D1C5CHFA_enTW969TW969%26oq%3Dgoogle%2B%25E7%2599%25BB%25E5%2585%25A5%26gs_lcrp%3DEgZjaHJvbWUyBggAEEUYOTIGCAEQRRhA0gEIMzg4NmowajeoAgCwAgA%26sourceid%3Dchrome%26ie%3DUTF-8&ec=GAZAAQ&hl=zh-TW&ifkv=ASKXGp3QryzAjE0knNfUu47LhOa7xamGWPzdQyIIFxDn6N_DP-3gX4AX1aOH7NpEH8LoWhyn-25R&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S486807008%3A1702536821223868&theme=glif'
    driver.get(url)

    driver.find_element(By.ID, "identifierId").send_keys(email)
    time.sleep(3)
    driver.find_element(
        By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]').click()
    time.sleep(3)
    driver.find_element(
        By.XPATH, '//input[@name="Passwd"]').send_keys(password)
    driver.find_element(
        By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]').click()
    return driver


if __name__ == '__main__':
    print("Start Chrome With Profile")
    driver = start_chrome_with_profile(
        # user_data_dir='/Users/chungilin/Library/Application Support/Google/Chrome/SeleniumUserProfile',
        # profile_dir='Profile 3'

        user_data_dir='./chrome_profile',
        profile_dir='Profile 3'
    )
    time.sleep(3)

    print("Semi Login")
    uc_driver = start_chrome_with_semi_auto_login(
        os.getenv("gmail"), os.getenv("gmail_pwd"))
    time.sleep(10)

    print("Closeing driver...")
    driver.quit()
    uc_driver.quit()
    print("Done")
