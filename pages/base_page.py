from typing import Callable, Dict

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.page_object import PageObject


class BaseLocators:
    next_step_button_xpath = "//button[normalize-space()='Next Step' and not(@disabled)]"
    loading_cover_xpath = "//div[contains(@class,'loading-cover')]"


class BasePage(PageObject):
    URL_SUFFIX: str = "/sign-up/carrier"
    page_verification_elements: Dict[str, WebElement]

    def __init__(self, browser, base_url):
        super().__init__(browser)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = BaseLocators

    def navigate_to(self) -> None:
        self.driver.get(self.url)
        self.log.debug(f"Navigate to page: {self.url}")
        self.wait_for_app_load()

    def check_if_on_page(self) -> None:
        self.check_if_actual_url_equals_expected()

    def check_if_actual_url_equals_expected(self):
        current_url = self.driver.current_url
        assert (
                self.driver.current_url == self.url
        ), f"Expected URL: {self.url}, actual URL: {current_url}"
        self.log.info(f'On page "{current_url}"')

    def wait_for_url_change(self, timeout=None) -> None:
        self.log.info(f'URL to change: "{self.url}"')
        self.driver.wait(timeout).until(
            EC.url_changes(self.url),
            f'Url "{self.url}" has not changed in {timeout} seconds timeout',
        )
        self.log.info(f'URL after: "{self.driver.current_url}"')

    def wait_for_app_load(self):
        self.driver.wait_for_element_hide(xpath=self.locators.loading_cover_xpath)

    def add_element_to_verification(self, element: Callable[[], WebElement]):
        if not hasattr(self, "page_verification_elements"):
            self.page_verification_elements = {}
        try:
            self.page_verification_elements[element.__name__] = element()
        except TimeoutException:
            self.log.error(
                'Can\'t reach element "%(element_name)s"',
                dict(element_name=element.__name__),
            )
            raise

    def seed_page_verification_elements(self) -> None:
        raise NotImplementedError("Page elements verification list was not initialized")

    def verify_page_elements(self) -> None:
        if not hasattr(self, "page_verification_elements"):
            self.seed_page_verification_elements()
        for name, webelement in self.page_verification_elements.items():
            assert webelement.is_displayed(), f"{name} NOT DISPLAYED"
            self.log.info(f"{name} DISPLAYED")
        self.log.info("Page elements verification OK")

    def next_button(self) -> WebElement:
        return self.get_element_by_xpath(self.locators.next_step_button_xpath)
