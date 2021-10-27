from abc import ABC, abstractmethod
from typing import Union

import webdriverwrapper


class WebBrowser(ABC):
    """Abstraction of a web browser."""

    @abstractmethod
    def driver(self) -> Union[webdriverwrapper.Chrome, webdriverwrapper.Firefox]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class WebBrowserError(Exception):
    """Represent web browser error."""

    pass
