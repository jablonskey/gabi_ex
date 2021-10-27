from pages.base_page import BaseLocators, BasePage


class NamePageLocators(BaseLocators):
    first_name_form_xpath = "//div[contains(@class,'firstNameField')]//input"
    first_name_invalid_info_xpath = f"{first_name_form_xpath}/parent::*/following-sibling::span[contains(@class,'textError')]"
    last_name_form_xpath = "//div[contains(@class,'lastNameField')]//input"
    last_name_invalid_info_xpath = f"{last_name_form_xpath}/parent::*/following-sibling::span[contains(@class,'textError')]"


class NamePage(BasePage):
    URL_SUFFIX: str = "/sign-up/name"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = NamePageLocators
        self.INVALID_FIRST_NAME = "A"
        self.VALID_FIRST_NAME = "ValidFirstName"
        self.INVALID_LAST_NAME = "A"
        self.VALID_LAST_NAME = "Valid Last Name"

        self.NOT_VALID_INFO = "Not valid"

        self.FIRST_NAME_SPECIAL_CHARS_VALIDATION_INFO = "First name should not contain special characters."
        self.FIRST_NAME_TWO_CHARS_VALIDATION_INFO = "First name should contain at least two chars."
        self.LAST_NAME_TWO_CHARS_VALIDATION_INFO = "Last name should contain at least two chars."

    def seed_page_verification_elements(self):
        self.add_element_to_verification(self.first_name_form)
        self.add_element_to_verification(self.last_name_form)

    def first_name_form(self):
        return self.get_element_by_xpath(self.locators.first_name_form_xpath)

    def first_name_invalid_info(self):
        return self.get_element_by_xpath(self.locators.first_name_invalid_info_xpath)

    def last_name_form(self):
        return self.get_element_by_xpath(self.locators.last_name_form_xpath)

    def last_name_invalid_info(self):
        return self.get_element_by_xpath(self.locators.last_name_invalid_info_xpath)