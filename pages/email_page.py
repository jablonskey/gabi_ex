from pages.base_page import BaseLocators, BasePage


class EmailPageLocators(BaseLocators):
    email_doublecheck_info_xpath = "//div[contains(@class,'EmailStep') and contains(@class,'textError')]//span"
    email_form_xpath = "//input[@name='email' and contains(@class,'GabiInput')]"
    email_form_invalid_info_xpath = f"{email_form_xpath}/parent::*/following-sibling::span[contains(@class,'textError')]"


class EmailPage(BasePage):
    URL_SUFFIX: str = "/sign-up/email"
    TEMP_EMAIL_ADDRESS = "temp@email.com"
    VALID_BUT_INCORRECT_EMAIL_ADDRESS = "asd@asd.com"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = EmailPageLocators

    def seed_page_verification_elements(self) -> None:
        self.add_element_to_verification(self.next_button)

    def fill_temp_email(self):
        self.email_form().send_keys(self.TEMP_EMAIL_ADDRESS)

    def email_form(self):
        return self.get_element_by_xpath(self.locators.email_form_xpath)

    def email_form_invalid_info(self):
        return self.get_element_by_xpath(self.locators.email_form_invalid_info_xpath)

    def email_doublecheck_info(self):
        return self.get_element_by_xpath(self.locators.email_doublecheck_info_xpath)

    def drop_focus_from_form(self):
        self.get_element_by_xpath("//body").click()