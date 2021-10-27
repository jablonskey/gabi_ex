import pytest_check as check

from actions.actions import Actions


def test_check_name_forms_validation(browser, base_url):
    actions = Actions(browser, base_url)
    actions.insurnace_choice_page.navigate_to()
    actions.insurnace_choice_page.verify_page_elements()
    actions.choose_no_insurance()

    actions.name_page.first_name_form().send_keys("A")
    actions.name_page.last_name_form().click()

    check.equal(actions.name_page.first_name_invalid_info().text,
                actions.name_page.FIRST_NAME_TWO_CHARS_VALIDATION_INFO)

    actions.name_page.first_name_form().clear()
    check.equal(actions.name_page.first_name_invalid_info().text,
                actions.name_page.NOT_VALID_INFO)

    actions.name_page.first_name_form().send_keys("INVALID_NAME")
    check.equal(actions.name_page.first_name_invalid_info().text,
                actions.name_page.FIRST_NAME_SPECIAL_CHARS_VALIDATION_INFO)

    actions.enter_valid_first_name()
    actions.check_if_first_name_verified_as_valid()

    actions.name_page.last_name_form().send_keys("A")
    check.equal(
        actions.name_page.last_name_invalid_info().text,
        actions.name_page.LAST_NAME_TWO_CHARS_VALIDATION_INFO)
    actions.name_page.last_name_form().clear()
    check.equal(actions.name_page.last_name_invalid_info().text,
                actions.name_page.NOT_VALID_INFO)
    actions.enter_valid_last_name()
    actions.check_if_last_name_verified_as_valid()


def test_full_signup_flow(browser, base_url):
    actions = Actions(browser, base_url)
    actions.insurnace_choice_page.navigate_to()
    actions.choose_no_insurance()
    actions.fill_names_and_proceed()
    actions.fill_temp_address_and_proceed()
    actions.skip_hdyhau()
    actions.fill_temp_email_address_and_proceed()
    actions.fill_temp_phone_number_and_proceed()
    actions.check_if_verification_reached()

