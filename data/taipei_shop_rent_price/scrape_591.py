# This file would intercept the XHR request of shop front data of www.591.tw
#
# Note:
# - The process respect www.591.com.tw website permission (i.e. robots.txt)
# - Please use the code for education purpose or reference only,
#   don't use the code to exploit or do something harmful for the company
# - Each scrape is different, this approach is the pragmatic approach with
#   only one connection running sequentially (which is a good approach for this
#   case). For more scalable design (in Python) you could explore scrapy
#   framework.

import os
import sys; sys.stderr = object #hacky way to silent thread response fail
import time

from typing import Callable
from random import random

from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(CURRENT_DIR, 'download/591_xhr_responses.txt')


class WebExplorer:
    def __init__(self, driver_obj: object):
        self.driver = driver_obj
        self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)

    def get(self, url):
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


class WebExplorer591(WebExplorer):
    def __init__(self, driver_obj: object, url: str):
        self.driver = driver_obj
        super().__init__(self.driver)

        if url:
            self.get(url)

    def choose_initial_popup(self, town: str):
        return self.wait_and_click((By.XPATH, '//div/dl/dd'), lambda x: town in x.text)

    def close_pop_up(self):
        return self.wait_and_click((By.XPATH, '//div/a[@class="close"]'))

    def choose_search_category(self, category: str):
        return self.wait_and_click(
            (By.XPATH, '//div/a[contains(@class, "auto-type-tab") and contains(@class, "auto-tab-business")]'),
            lambda x: category in x.text
        )

    def choose_filter_town(self, town: str):
        try:
            focus = self.wait.until(ec.presence_of_element_located(
                (By.XPATH, '//div/span[@class="select" and @data-text="0"]')
            ))

            if not (town in focus.text):
                self.wait_and_click(self.wait, (By.XPATH, '//div/span[@class="select" and @data-text="0"]'))
                self.wait_and_click(self.wait,
                    (By.XPATH, '//ul[@id="optionBox"]//a[@data-type="region"]'),
                    lambda x: town in x.text
                )

            return True

        except Exception:
            return False

    def click_next_button(self):
        return self.wait_and_click(
            (By.XPATH, '//div/a[@class="pageNext"]'),
            lambda x: x.get_attribute('href')
        )


if __name__ == '__main__':
    # set webdriver, request interceptor scope, and wait object
    print("INFO: setup crawler, use Chrome driver")
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.headless = True

    driver = webdriver.Chrome(options=webdriver_options)
    url_regex = '.*business\.591\.com\.tw\/home\/search\/rsList\?.*'
    driver.scopes = [
        url_regex
    ]
    start_url = 'https://www.591.com.tw/'

    web_explorer = WebExplorer591(driver, start_url)

    # start page as new guest
    print("INFO: starting the crawler")
    web_explorer.choose_initial_popup('台北')
    web_explorer.close_pop_up()

    # arrived at homepage, go to the search category, front shop
    web_explorer.choose_search_category('店面')
    web_explorer.close_pop_up()
    web_explorer.choose_filter_town('台北')
    web_explorer.close_pop_up()

    # starting to get data
    print("INFO: starting to get data")
    last_page_num = web_explorer.get_last_page_num()
    current_page_num = 1
    while True:
        if last_page_num:
            print("INFO: getting data for page {} of {}".format(
                current_page_num, last_page_num))
        else:
            print("INFO: getting data for page {}".format(current_page_num))

        time.sleep(3) # friendly for the server
        driver.wait_for_request(url_regex)
        print("INFO: page {} finished, moving to next page...".format(current_page_num))

        web_explorer.scroll_down_until_end()
        current_page_num = current_page_num + 1

        next_page_available = web_explorer.click_next_button()

        if not next_page_available:
            break

    print("INFO: seems like no more next page, wrapping data") 
    web_explorer.save_all_responses(OUTPUT_PATH, 'utf-8')

    driver.close()
    print('INFO: getting data from {} finished. File saved on {}'
        .format(start_url, OUTPUT_PATH))
