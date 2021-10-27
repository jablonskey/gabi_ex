from typing import Callable, Dict

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from pages.page_object import PageObject


class BaseLocators:
    next_step_button_xpath = "//button[normalize-space(text()='Next Step')]"
    loading_cover_xpath = "//div[contains(@class,'loading-cover')]"


class BasePage(PageObject):
    URL_SUFFIX: str = "/sign-up/carrier"
    page_verification_elements: Dict[str, WebElement]

    def __init__(self, browser, base_url):
        super().__init__(browser)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = BaseLocators

    def navigate_to(self) -> None:
        self.driver.get(self.url)
        self.log.debug(f"Navigate to page: {self.url}")
        self.wait_for_app_load()

    def wait_for_app_load(self):
        loading_cover = self.get_element_by_xpath(self.locators.loading_cover_xpath)
        self.wait_for_element_hide(loading_cover)

    def add_element_to_verification(self, element: Callable[[], WebElement]):
        if not hasattr(self, "page_verification_elements"):
            self.page_verification_elements = {}
        try:
            self.page_verification_elements[element.__name__] = element()
        except TimeoutException:
            self.log.error(
                'Can\'t reach element "%(element_name)s"',
                dict(element_name=element.__name__),
            )
            raise

    def seed_page_verification_elements(self) -> None:
        raise NotImplementedError("Page elements verification list was not initialized")

    def verify_page_elements(self) -> None:
        if not hasattr(self, "page_verification_elements"):
            self.seed_page_verification_elements()
        for name, webelement in self.page_verification_elements.items():
            assert webelement.is_displayed(), f"{name} NOT DISPLAYED"
            self.log.info(f"{name} DISPLAYED")
        self.log.info("Page elements verification OK")


class InsuracePageLocators(BaseLocators):
    no_insurance_button_xpath = "//button[normalize-space()='I Don’t Have Insurance']"


class InsuranceChoicePage(BasePage):

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url = f"{base_url}{self.URL_SUFFIX}"
        self.locators = InsuracePageLocators

    def seed_page_verification_elements(self):
        self.add_element_to_verification(self.no_insurance_button)

    def no_insurance_button(self):
        return self.get_element_by_xpath(self.locators.no_insurance_button_xpath)


class NamePageLocators:
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
