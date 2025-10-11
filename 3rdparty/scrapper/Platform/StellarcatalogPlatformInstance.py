from functools import lru_cache

import Platform.StellarcatalogCfg as pltCfg
from ContentExtractor.ContentExtractorInterface import ContentExtractorInterface
from ContentExtractor.HtmlExtractor import HtmlExtractor
from Scrapper.ScrapperInterface import ScrapperInterface
from Scrapper.StellarcatalogScrapper import StellarcatalogScrapper
from SolarSystemDataHolder.DataHolderInterface import DataHolderInterface
from SolarSystemDataHolder.StellarcatalogDataHolder import StellarcatalogDataHolder
from WebRequester.WebRequester import WebRequester
from WebRequester.WebRequesterInterface import WebRequesterInterface


@lru_cache(maxsize=1)
def GetSolarSystemDataHolderInstance() -> DataHolderInterface:
    return StellarcatalogDataHolder()


@lru_cache(maxsize=1)
def __getHtmlExtractorInstance() -> ContentExtractorInterface:
    return HtmlExtractor()


@lru_cache(maxsize=1)
def __getWebRequesterInstance() -> WebRequesterInterface:
    return WebRequester()


@lru_cache(maxsize=1)
def GetScrapperInstance() -> ScrapperInterface:
    return StellarcatalogScrapper(
        __getHtmlExtractorInstance(),
        __getWebRequesterInstance(),
        pltCfg.MAIN_URL,
        pltCfg.CATALOG_URL,
        pltCfg.OFFSET_CATALOG,
        pltCfg.STARS_TYPE
    )
