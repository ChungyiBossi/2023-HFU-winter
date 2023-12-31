from selenium.webdriver.remote.webdriver import By
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys


class ChatGPTParser:
    def __init__(self,
                 driver,
                 gpt_url: str = 'https://chat.openai.com/'):
        """ ChatGPT parser
        Args:
            driver_path (str, optional): The path of the chromedriver.
            gpt_url (str, optional): The url of ChatGPT.
        """
        # Start a webdriver instance and open ChatGPT
        self.driver = driver
        self.driver.get(gpt_url)

    @staticmethod
    def get_driver(driver_path: str = None,):
        chrome_options = uc.ChromeOptions()
        # chrome_options.set_capability("detach", True)
        return uc.Chrome(options=chrome_options, enable_cdp_events=True) if driver_path is None else uc.Chrome(driver_path, options=chrome_options)

    def __call__(self, msg: str):
        # Find the input field and send a question
        input_field = self.driver.find_elements(
            By.TAG_NAME, 'textarea')[0]
        input_field.send_keys(msg)
        input_field.send_keys(Keys.RETURN)

    def read_respond(self):
        try:
            response = self.driver.find_elements(By.TAG_NAME, 'p')[-2].text
            return response
        except:
            return None

    def new_chat(self):
        self.driver.find_element(By.XPATH, '//a[text()="New chat"]').click()

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    import time
    driver = ChatGPTParser.get_driver()
    gpt_parser = ChatGPTParser(driver)
    x = input("Waiting for google login")  # 用input 卡住
    query = "1+1=?"
    gpt_parser(query)  # send the query
    time.sleep(1)
    response = gpt_parser.read_respond()  # response = 2

    print(response)
