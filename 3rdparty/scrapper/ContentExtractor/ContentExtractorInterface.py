from abc import ABC, abstractmethod
from typing import List, Tuple


class StarWebside:
    """Represents a website related to star
    Attributes:
        starName (str): Star name
        link(str): URL to website
    """

    def __init__(self, starName: str, link: str) -> None:
        self.starName: str = starName
        self.link: str = link

    def __str__(self) -> str:
        return self.starName + " -> " + self.link


class ContentExtractorInterface(ABC):
    """An interface defining methods for extracting astronomical content
    such as star systems, stars and planets and from website HTML pages.
    """

    @abstractmethod
    def extractStarLink(self, html: str) -> List[StarWebside]:
        """Extracts links to stars pages from provided HTML source code.
        Args:
            html (str): Raw HTML source code containing star list
        Returns:
            List[StarWebside]: A list of StarWebside objects,
                each containing name of star and URL to page.
        """
        pass

    @abstractmethod
    def extractPlanetLink(self, mainLink: str, html: str) -> List[StarWebside]:
        """Extracts links to planet pages belonging to a specific star system.
        Args:
            mainLink (str): The base URL of the current star system page.
            html (str): Raw HTML source code containing planet list.
        Returns:
            List[StarWebside]: A list of StarWebside objects representing planets,
            each containing the planet name and its page link.
        """
        pass

    @abstractmethod
    def checkContent(self, html: str) -> bool:
        """Checks whether the provided HTML content is valid and can be parsed.
        Args:
            html (str): HTML content to verify.
        Returns:
            bool: True if the content structure matches the expected format.
            False otherwise.
        """
        pass

    @abstractmethod
    def extractSystemName(self, html: str) -> str:
        """Extracts the name of the star system from the HTML page.
        Args:
            html (str): HTML content of the star system page.
        Returns:
            str: The name of the star system.
        """
        pass

    @abstractmethod
    def extractStars(self, html: str) -> Tuple[bool, dict, List[dict]]:
        """Extracts data about all stars in a given star system.
        Args:
            html (str): HTML content of the star system page.
        Returns:
            Tuple[bool, dict, List[dict]]:
            - bool: Indicates whether any stars were found.
            - dict: General information about the system.
            - List[dict]: A list of dictionaries containing detailed data for each star.
        """
        pass

    @abstractmethod
    def extractPlanet(self, html: str) -> dict:
        """Extracts detailed information about a single planet from its HTML page.
        Args:
            html (str): HTML content of the planet's page.
        Returns:
            dict: A dictionary containing planet parameters
        """
        pass
