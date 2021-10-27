import logging

import pytest_check as check

from browsers import WebBrowser
from pages.base_page import InsuranceChoicePage, NamePage


class Actions:
    def __init__(self, browser: WebBrowser, base_url):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.insurnace_choice_page = InsuranceChoicePage(browser, base_url)
        self.name_page = NamePage(browser, base_url)

    def choose_no_insurance(self):
        self.insurnace_choice_page.no_insurance_button().click()

    def enter_invalid_first_name(self):
        self.name_page.first_name_form().clear()
        self.name_page.first_name_form().send_keys(self.name_page.INVALID_FIRST_NAME)

    def check_if_first_name_verified_as_valid(self):
        check.is_true(self.name_page.is_element_not_visible_by_xpath(
            self.name_page.locators.first_name_invalid_info_xpath))

    def enter_valid_first_name(self):
        self.name_page.first_name_form().clear()
        self.name_page.first_name_form().send_keys(self.name_page.VALID_FIRST_NAME)

    def enter_invalid_last_name(self):
        self.name_page.last_name_form().clear()
        self.name_page.last_name_form().send_keys(self.name_page.INVALID_LAST_NAME)

    def check_if_last_name_verified_as_invalid(self):
        assert self.name_page.is_element_visible_by_xpath(
            self.name_page.last_name_invalid_info())

    def enter_valid_last_name(self):
        self.name_page.last_name_form().clear()
        self.name_page.last_name_form().send_keys(self.name_page.VALID_LAST_NAME)

    def check_if_last_name_verified_as_valid(self):
        check.is_true(self.name_page.is_element_not_visible_by_xpath(
            self.name_page.locators.last_name_invalid_info_xpath))
