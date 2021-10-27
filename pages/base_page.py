from typing import Callable, Dict

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.page_object import PageObject


class BaseLocators:
    next_step_button_xpath = "//button[normalize-space()='Next Step' and not(@disabled)]"
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

    def check_if_on_page(self) -> None:
        self.check_if_actual_url_equals_expected()

    def check_if_actual_url_equals_expected(self):
        current_url = self.driver.current_url
        assert (
                self.driver.current_url == self.url
        ), f"Expected URL: {self.url}, actual URL: {current_url}"
        self.log.info(f'On page "{current_url}"')

    def wait_for_url_change(self, timeout=None) -> None:
        self.log.info(f'URL to change: "{self.url}"')
        self.driver.wait(timeout).until(
            EC.url_changes(self.url),
            f'Url "{self.url}" has not changed in {timeout} seconds timeout',
        )
        self.log.info(f'URL after: "{self.driver.current_url}"')

    def wait_for_app_load(self):
        self.driver.wait_for_element_hide(xpath=self.locators.loading_cover_xpath)

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

    def next_button(self) -> WebElement:
        return self.get_element_by_xpath(self.locators.next_step_button_xpath)


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


class AddressPageLocators(BaseLocators):
    address_search_first_result_xpath = "//div[contains(@class,'SmartyStreetsAutocomplete')]/button[1]//div[contains(@class,'HoverIndicator')]"
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


class EmailPageLocators(BaseLocators):
    email_form_xpath = "//input[@name='email' and contains(@class,'GabiInput')]"


class EmailPage(BasePage):
    URL_SUFFIX: str = "/sign-up/email"
    TEMP_EMAIL_ADDRESS = "temp@email.com"

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
