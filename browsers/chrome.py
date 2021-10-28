import logging

import webdriverwrapper
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType, os_name, OSType

from browsers import WebBrowser


class Chrome(WebBrowser):

    def __init__(self, headless_flag) -> None:
        chrome_options: options = Options()
        chrome_options.add_argument("--allow-insecure-localhost")
        chrome_options.add_argument("--remote-debugging-port=9222")

        chrome_options.add_experimental_option(
            "perfLoggingPrefs",
            {
                "enableNetwork": True,
                "enablePage": False,
                "traceCategories": "browser,devtools.timeline,devtools,network",
            },
        )
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if headless_flag:
            LOGGER.setLevel(logging.ERROR)
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--log-level=4")

        capabilities = webdriverwrapper.DesiredCapabilities().CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        capabilities["acceptInsecureCerts"] = True

        if os_name() == OSType.LINUX:
            self.chrome = webdriverwrapper.Chrome(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                options=chrome_options,
                desired_capabilities=capabilities,

            )
        else:
            self.chrome = webdriverwrapper.Chrome(
                ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                options=chrome_options,
                desired_capabilities=capabilities,

            )

    def driver(self):
        return self.chrome

    def name(self) -> str:
        return "Chrome"
