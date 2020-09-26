from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from . import WebExplorer


class WebExplorer591(WebExplorer):
    def __init__(self, driver_obj: object, url: str):
        self.driver = driver_obj
        self.url = url
        super().__init__(self.driver, self.url)

    def check_page_error(self) -> bool:
        if self.find_a_web_element_obj((By.XPATH, '//div[@class="error-info"]')):
            return True
        else:
            False

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

    def initial_guest_page_to_home_page(self, select_city: str, select_category: str) -> None:
        # start page as new guest
        print("INFO: setup the initial guest state")
        self.choose_initial_popup(select_city)
        self.close_pop_up()

        # arrived at homepage, go to the search category, front shop
        self.choose_search_category(select_category)
        self.close_pop_up()
        self.choose_filter_town(select_city)
        self.close_pop_up()
        print("INFO: arriving at the selected homepage")

    def go_to_page_id(self, post_id: int) -> None:
        url = 'https://rent.591.com.tw/rent-detail-{}.html'.format(post_id)
        self.get(url)
