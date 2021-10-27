import logging

import pytest

from browsers.chrome import Chrome
from browsers.firefox import Firefox

_BASE_URL: str = "https://staging.gabi.com"
DEFAULT_IMPLICIT_WAIT_TIME: int = 1


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        type=str,
        choices=["chrome", "firefox"],
        default="chrome",
    )
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture(scope="function")
def browser(request):
    browser_parameter = request.config.option.browser
    logging.info(f'option.browser = "{browser_parameter}"')
    headless_flag = request.config.option.headless
    logging.info(f'option.headless = "{headless_flag}"')

    if browser_parameter == "chrome":
        session_browser = Chrome(headless_flag)
    else:
        session_browser = Firefox(headless_flag)

    session_browser.driver().maximize_window()
    session_browser.driver().implicitly_wait(DEFAULT_IMPLICIT_WAIT_TIME)

    yield session_browser

    session_browser.driver().quit()


@pytest.fixture(scope="session")
def base_url(request) -> str:
    return _BASE_URL
