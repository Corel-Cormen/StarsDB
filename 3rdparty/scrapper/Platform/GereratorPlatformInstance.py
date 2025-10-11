from functools import lru_cache

from Scrapper.ScrapperInterface import ScrapperInterface
from Scrapper.GeneratorScrapper import GeneratorScrapper
from SolarSystemDataHolder.DataHolderInterface import DataHolderInterface
from SolarSystemDataHolder.StellarcatalogDataHolder import StellarcatalogDataHolder


@lru_cache(maxsize=1)
def GetSolarSystemDataHolderInstance() -> DataHolderInterface:
    return StellarcatalogDataHolder()


@lru_cache(maxsize=1)
def GetScrapperInstance() -> ScrapperInterface:
    return GeneratorScrapper()
