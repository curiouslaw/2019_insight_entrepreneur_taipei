import time

from typing import Callable
from random import random

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class WebExplorer:
    def __init__(self, driver: object):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)

    def get(self, url: str):
        self.driver.get(url)

    def wait_and_click(self, locator_obj: object,
        *lambda_filter: Callable, is_display: bool = True,
        delay: float = 0.5, retry: int = 1) -> bool:
        """
        Wait for the presence of certain located object, apply lambda filter,
        and click the first clickable object found

        Args:
            locator_obj (object): selenium locator object
            *lambda_filter (function): series of lambda functions that would
                applied to the list of s“elected selenium WebElement object
            is_display (bool, optional): only look at object that is displayed to
                the user. Defaults to True.
            delay(float, optional): first delay before do any action

        Do:
            Get selenium WebElement objects after applying locator_obj
                and lambda_filter function (if exist) and click them. if any error
                occur would try n (retry arg) time(s) on all of the function.
        """
        wait_interval = (((0.5 - random()) * 2) * (0.2 * delay)) + delay

        try:
            focus = self.wait.until(ec.presence_of_all_elements_located(locator_obj))
            focus = [x for x in focus if x.is_displayed()]

            if lambda_filter:
                for f in lambda_filter:
                    focus = filter(f, focus)

                focus = next(focus)
                time.sleep(wait_interval)
                focus.click()
                return True

            if focus:
                time.sleep(wait_interval)
                focus[0].click()
                return True

        # exception catch anything, include timeout error and no object found
        except Exception as e:
            if retry:
                print("INFO: {} occured! will retry {} times".format(e, retry))
                self.wait_and_click(self.wait, locator_obj, lambda_filter,
                retry=retry - 1)

            print("ERROR: {} occured, stop running function".format(e))
            return False

    def get_web_elements_obj(self, locator_obj: object) -> list:
        try:
            return self.wait.until(ec.presence_of_all_elements_located(locator_obj))
        except Exception:
            return False

    def scroll_down_until_end(self, page_down_delay: float = 0.2, stop_until: float = 0.95):
        document_height = self.driver.execute_script("return document.body.scrollHeight")
        target_height_threshold = stop_until * document_height
        page_down_action = self.action.send_keys(Keys.PAGE_DOWN)

        page_down_y_move = 700

        click_repeat = int(target_height_threshold / page_down_y_move) + 1

        for i in range(click_repeat):
            page_down_action.perform()
            time.sleep(page_down_delay)

    def save_all_responses(self, filepath: str, decoder: str):
        with open(filepath, 'w') as f:
            for x in self.driver.requests:
                f.write(x.response.body.decode(decoder) + '\n')

    def get_last_page_num(self):
        focus = self.get_web_elements_obj(
            (By.XPATH, '(//div[@class="pageBar"]/a[@class="pageNum-form"])[last()]')
        )
        if focus:
            return focus[0].text
        else:
            return False
