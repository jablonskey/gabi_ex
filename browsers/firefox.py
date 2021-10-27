import logging

import webdriverwrapper
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from browsers import WebBrowser


class Firefox(WebBrowser):
    """Representation of a firefox web browser."""

    def __init__(self) -> None:
        firefox_options = Options()
        firefox_options.log.level = "trace"

        self.firefox = webdriverwrapper.Firefox(
            executable_path=GeckoDriverManager().install(),
            options=firefox_options,

        )

        logging.debug(f"Firefox version: {self.firefox.capabilities['browserVersion']}")

    def driver(self):
        return self.firefox

    def name(self) -> str:
        return "Firefox"
