# noinspection PyPep8Naming
import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


class PageObject:
    def __init__(self, browser):
        self.driver = browser.driver()
        self.log = logging.getLogger(self.__class__.__name__)

    def get_element_by_xpath(self, xpath, timeout_in_seconds=None) -> WebElement:
        try:
            self.driver.wait_for_element_show(xpath=xpath, timeout=timeout_in_seconds)
        except TimeoutException:
            self.log.error(
                'Element with xpath =  "%(xpath)s" is not visible. Timeout: %(timeout)s seconds.',
                dict(
                    xpath=xpath,
                    timeout=(
                        timeout_in_seconds
                        if timeout_in_seconds
                        else self.driver.default_wait_timeout
                    ),
                ),
            )
            raise
        return self.driver.get_elm(xpath=xpath)

    def is_element_visible_by_xpath(self, xpath, timeout_in_seconds=None) -> bool:
        if not timeout_in_seconds:
            timeout_in_seconds = 1
        try:
            self.driver.wait_for_element(timeout=timeout_in_seconds, xpath=xpath)
            self.scroll_to(self.get_element_by_xpath(xpath))
            self.driver.wait_for_element_show(timeout=timeout_in_seconds, xpath=xpath)
            self.log.info(
                'Element with xpath =  "%(xpath)s" visible as expected.',
                dict(xpath=xpath),
            )
            return True
        except TimeoutException:
            self.log.info(
                'Element with xpath =  "%(xpath)s" is not visible. Timeout: %(timeout)s seconds. Expected visible',
                dict(
                    xpath=xpath,
                    timeout=(
                        timeout_in_seconds
                        if timeout_in_seconds
                        else self.driver.default_wait_timeout
                    ),
                ),
            )
            return False

    def wait_for_element_hide(self, element: WebElement):
        self.driver.wait().until(EC.invisibility_of_element(element))

    def wait_for_element_show(self, element: WebElement, timeout_in_seconds=None):
        self.driver.wait(timeout=timeout_in_seconds).until(EC.visibility_of(element))

    def is_element_not_visible_by_xpath(self, xpath, timeout_in_seconds=None) -> bool:
        if not timeout_in_seconds:
            timeout_in_seconds = 1
        try:
            self.driver.wait_for_element_hide(timeout=timeout_in_seconds, xpath=xpath)
            self.log.info(
                'Element with xpath =  "%(xpath)s" is not visible as expected.',
                dict(xpath=xpath),
            )
            return True
        except TimeoutException:
            self.log.info(
                'Element with xpath =  "%(xpath)s" is not hidden. Expected hidden.',
                dict(xpath=xpath),
            )
            return False

    def scroll_to(self, element: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        self.wait_for_element_show(element)
