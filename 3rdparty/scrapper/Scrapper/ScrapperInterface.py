from abc import ABC, abstractmethod

from SolarSystemDataHolder.DataHolderInterface import DataHolderInterface


class ScrapperInterface(ABC):
    """An interface defining methods for scrap and save stars/planets data.
    """

    @abstractmethod
    def scrap(self, dataHolder: DataHolderInterface) -> bool:
        """Method for scrap stars/planets data
        Returns:
            bool: status
        """
        pass
