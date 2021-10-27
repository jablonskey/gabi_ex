from pages.base_page import BaseLocators, BasePage


class HdyhauPageLocators(BaseLocators):
    skip_button_xpath = "//button[normalize-space()='Skip' and not(@disabled)]"


class HdyhauPage(BasePage):
    URL_SUFFIX: str = "/sign-up/hdyhau"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = HdyhauPageLocators

    def seed_page_verification_elements(self) -> None:
        self.add_element_to_verification(self.next_button)

    def skip_button(self):
        return self.get_element_by_xpath(self.locators.skip_button_xpath)