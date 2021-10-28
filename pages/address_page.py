from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BaseLocators, BasePage


class AddressPageLocators(BaseLocators):
    address_search_first_result_xpath = "//div[contains(@class,'SmartyStreetsAutocomplete')]/button//div[contains(@class,'HoverIndicator')]"
    address_search_modal_xpath = "//div[contains(@class,'modalContent') and contains(@class,'GabiAddressField')]"
    address_form_xpath = "//input[@name='address_field_input']"


class AddressPage(BasePage):
    URL_SUFFIX: str = "/sign-up/address"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = AddressPageLocators

    def seed_page_verification_elements(self) -> None:
        self.add_element_to_verification(self.address_form)
        self.add_element_to_verification(self.next_button)

    def fill_temp_address(self):
        self.address_form().click()
        self.wait_for_element_show(self.address_search_modal())
        self.address_search_form().send_keys("123")
        self.wait_for_search_results()
        self.choose_first_result()
        self.driver.wait_for_element_hide(
            xpath=self.locators.address_search_modal_xpath)

    def address_form(self) -> WebElement:
        return self.get_element_by_xpath(self.locators.address_form_xpath)

    def address_search_form(self) -> WebElement:
        return self.get_element_by_name("address-placeholder")

    def address_search_modal(self):
        return self.get_element_by_xpath(self.locators.address_search_modal_xpath)

    def wait_for_search_results(self):
        self.driver.wait_for_element_show(
            xpath=self.locators.address_search_first_result_xpath)

    def address_search_first_result(self):
        return self.get_element_by_xpath(
            self.locators.address_search_first_result_xpath)

    def choose_first_result(self):
        self.address_search_first_result().click()