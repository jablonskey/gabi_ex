from pages.base_page import BaseLocators, BasePage


class VerificationPageLocators(BaseLocators):
    verification_code_form_xpath = "//input[@name='lead.verification_code' and contains(@class,'GabiInput')]"


class VerificationPage(BasePage):
    URL_SUFFIX: str = "/sign-up/verification"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = VerificationPageLocators

    def seed_page_verification_elements(self) -> None:
        self.add_element_to_verification(self.next_button)
        self.add_element_to_verification(self.verification_code_form)

    def verification_code_form(self):
        return self.get_element_by_xpath(self.locators.verification_code_form_xpath)