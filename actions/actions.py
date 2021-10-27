import logging

import pytest_check as check

from browsers import WebBrowser
from pages.base_page import InsuranceChoicePage, NamePage, AddressPage, HdyhauPage, \
    EmailPage, PhonePage, VerificationPage


class Actions:
    def __init__(self, browser: WebBrowser, base_url):
        self.verification_page = VerificationPage(browser, base_url)
        self.phone_page = PhonePage(browser, base_url)
        self.email_page = EmailPage(browser, base_url)
        self.hdyhau_page = HdyhauPage(browser, base_url)
        self.adress_page = AddressPage(browser, base_url)
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

    def fill_names_and_proceed(self):
        self.enter_valid_first_name()
        self.enter_valid_last_name()
        self.name_page.next_button().click()
        self.name_page.wait_for_url_change()

    def fill_temp_address_and_proceed(self):
        self.adress_page.fill_temp_address()
        self.adress_page.next_button().click()
        self.adress_page.wait_for_url_change()

    def skip_hdyhau(self):
        self.hdyhau_page.skip_button().click()
        self.hdyhau_page.wait_for_url_change()

    def fill_temp_email_address_and_proceed(self):
        self.email_page.fill_temp_email()
        self.email_page.next_button().click()
        self.email_page.wait_for_url_change()

    def fill_temp_phone_number_and_proceed(self):
        self.phone_page.fill_temp_phone_number()
        self.phone_page.next_button().click()
        self.phone_page.wait_for_url_change()

    def check_if_verification_reached(self):
        self.verification_page.check_if_on_page()
