from pages.base_page import BaseLocators, BasePage


class PhonePageLocators(BaseLocators):
    phone_form_xpath = "//input[@name='phone_number' and contains(@class,'GabiInput')]"


class PhonePage(BasePage):
    URL_SUFFIX: str = "/sign-up/phone"
    TEMP_PHONE_NUMBER = "5555555777"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = PhonePageLocators

    def seed_page_verification_elements(self) -> None:
        self.add_element_to_verification(self.next_button)

    def fill_temp_phone_number(self):
        self.phone_form().send_keys(self.TEMP_PHONE_NUMBER)

    def phone_form(self):
        return self.get_element_by_xpath(self.locators.phone_form_xpath)