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
        default="firefox",
    )


@pytest.fixture(scope="function")
def browser(request):
    browser_parameter = request.config.option.browser
    logging.info(f'option.browser = "{browser_parameter}"')

    if browser_parameter == "chrome":
        session_browser = Chrome()
    else:
        session_browser = Firefox()

    session_browser.driver().maximize_window()
    session_browser.driver().implicitly_wait(DEFAULT_IMPLICIT_WAIT_TIME)

    yield session_browser

    session_browser.driver().quit()


@pytest.fixture(scope="session")
def base_url(request) -> str:
    return _BASE_URL
