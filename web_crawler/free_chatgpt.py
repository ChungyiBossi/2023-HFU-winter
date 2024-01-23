from google_login import start_chrome_with_semi_auto_login, start_chrome_with_profile
import os
import time
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    email = os.getenv('gmail')
    password = os.getenv('gmail_pwd')
    uc_driver = start_chrome_with_semi_auto_login(email, password)

    # Go to chatgpt
    uc_driver.get('https://chat.openai.com/')
    # Press Login
    uc_driver.find_element(
        By.XPATH,
        '//button[@data-testid="login-button"]').click()
    time.sleep(3)

    # Choose Chrome Login
    uc_driver.find_element(
        By.XPATH,
        '//button[@class="cf8ab1d76 ca5439885 c90865442"]').click()
    time.sleep(3)

    # Select Account
    uc_driver.find_element(
        By.XPATH,
        f'//div[@data-identifier="{email}"]').click()
    time.sleep(10)
    # # New Chat Not useable
    # x = uc_driver.find_element(
    #     By.XPATH, '//a[@class="group flex h-10 items-center gap-2 rounded-lg px-2 font-medium hover:bg-token-surface-primary"]').click()
    # time.sleep(5)

    text_list = ["How is your day?", "How old are you?",
                 "What is your favorite video game?"]

    input_area = uc_driver.find_element(By.TAG_NAME, "textarea")
    for t in text_list:
        # Send word to Textarea
        input_area.send_keys(t)
        input_area.send_keys(Keys.RETURN)

        try:
            response = uc_driver.find_elements(By.TAG_NAME, 'p')[-2].text
        except:
            time.sleep(2)
        time.sleep(5)

    time.sleep(10)
