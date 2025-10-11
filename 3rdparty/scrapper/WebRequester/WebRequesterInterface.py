from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple


class ReqStatus(Enum):
    OK = 0
    ERROR = 1
    NOT_EXIST = 2

class WebRequesterInterface(ABC):
    """An interface defining methods for web request.
    """

    @abstractmethod
    def getHTML(self, url: str) -> Tuple[ReqStatus, str]:
        """Get the content of web page by URL.
        Args:
            url (str): URL website
        Returns:
            Tuple[bool, str]:
                bool: status True/False
                str: HTML content
        """
        pass
