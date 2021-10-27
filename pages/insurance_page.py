from pages.base_page import BaseLocators, BasePage


class InsuraceChoicePageLocators(BaseLocators):
    no_insurance_button_xpath = "//button[normalize-space()='I Don’t Have Insurance']"


class InsuranceChoicePage(BasePage):

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = InsuraceChoicePageLocators

    def seed_page_verification_elements(self):
        self.add_element_to_verification(self.no_insurance_button)

    def no_insurance_button(self):
        return self.get_element_by_xpath(self.locators.no_insurance_button_xpath)