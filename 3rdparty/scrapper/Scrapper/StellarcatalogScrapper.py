from typing import List, Tuple

from ContentExtractor.ContentExtractorInterface import ContentExtractorInterface, StarWebside
from Scrapper.ScrapperInterface import ScrapperInterface
from WebRequester.WebRequesterInterface import WebRequesterInterface, ReqStatus
import SolarSystemDataHolder.DataHolderInterface as DH


class StellarcatalogScrapper(ScrapperInterface):

    def __init__(self,
                 contentExtractor: ContentExtractorInterface,
                 webRequester: WebRequesterInterface,
                 mainUrl: str,
                 catalogUrl: str,
                 offset: int,
                 starsType: List[Tuple[str, int]]) -> None:
        super().__init__()
        self.__contentExtractor: ContentExtractorInterface = contentExtractor
        self.__webRequester: WebRequesterInterface = webRequester
        self.__mainUrl: str = mainUrl
        self.__catalogUrl: str = catalogUrl
        self.__offset: int = offset
        self.__starsType: List[Tuple[str, int]] = starsType

    def scrap(self, dataHolder: DH.DataHolderInterface) -> bool:
        status, starsSystemLinks = self.__scrapSystemLinks()
        if status == True:
            status = self.__scrapSystemData(starsSystemLinks, dataHolder)
        return status

    def __scrapSystemLinks(self) -> Tuple[bool, List[str]]:
        starsSystemLinks = []
        result = True

        for starType in self.__starsType:
            sratIndexOffset = 0
            if result == False:
                break

            while (True):
                print(f"Indexing stars table: {starType[0]}/{sratIndexOffset}")
                reqStatus, html = self.__webRequester.getHTML(
                    self.__mainUrl + self.__catalogUrl.format(starType[1], sratIndexOffset))
                if reqStatus == ReqStatus.OK:
                    status = True
                else:
                    status = False

                if status:
                    starsWeb = self.__contentExtractor.extractStarLink(html)
                    if len(starsWeb) == 0:
                        print(f"End indexing: {starType[0]}")
                        break

                    for idx in range(len(starsWeb)):
                        if starsWeb[idx].link not in starsSystemLinks:
                            starsSystemLinks.append(starsWeb[idx].link)

                    sratIndexOffset += self.__offset
                else:
                    print("Error get website content in scrap system links function")
                    result = False
                    break

        return (result, starsSystemLinks)

    def __scrapSystemData(self, starsSystemLinks: List[str], dataHolder: DH.DataHolderInterface) -> bool:
        result = True

        counter = 0
        for systemLink in starsSystemLinks:
            counter += 1
            print(f"Scrap star system {counter}/{len(starsSystemLinks)}")

            reqStatus, html = self.__webRequester.getHTML(self.__mainUrl + systemLink)
            if reqStatus == ReqStatus.OK:
                result = True
            elif reqStatus == ReqStatus.NOT_EXIST:
                print("Website without content")
                continue
            else:
                print("Error get website content system data")
                result = False
                break

            if result == True:
                if self.__contentExtractor.checkContent(html):
                    systemName = self.__contentExtractor.extractSystemName(html)
                    isValid, location, stars = self.__contentExtractor.extractStars(html)
                    if isValid == True:
                        planetLinks = self.__contentExtractor.extractPlanetLink(systemLink, html)
                        result, planetDict = self.__createPlanets(planetLinks)
                        if result == False:
                            break
                        locationStruct = self.__createLocalization(location)
                        starStructList = self.__createStars(stars, planetDict)

                        system = DH.StarSystem(
                            systemName,
                            locationStruct,
                            starStructList,
                        )
                        dataHolder.starSystemList.append(system)
                    else:
                        print("Detect star system without location")
                else:
                    print("No HTML content to extract")

            else:
                print("Error get content in scrap system data function")
                result = False
                break

        return result

    def __createPlanets(self, planetLinks: List[StarWebside]) -> tuple[bool, dict[List[DH.Planet]]]:
        planetDict = {}
        result = True

        counter = 0
        for planetLink in planetLinks:
            counter += 1
            print(f"Scrap planet {counter}/{len(planetLinks)}")

            reqStatus, html = self.__webRequester.getHTML(self.__mainUrl + planetLink.link)
            if reqStatus == ReqStatus.OK:
                result = True
            elif reqStatus == ReqStatus.NOT_EXIST:
                print("Website without content")
                continue
            else:
                print("Error get website content in scrap planets")
                result = False
                break

            planetDictTmp = self.__contentExtractor.extractPlanet(html)
            planet = DH.Planet(
                planetDictTmp["Name"],
                planetDictTmp["Type"],
                planetDictTmp["Subtype"],
                planetDictTmp["Distance_from_the_star"],
                planetDictTmp["Orbit_around_star"],
                planetDictTmp["Eccentricity"],
                planetDictTmp["Mass"],
                planetDictTmp["Size"],
                planetDictTmp["Density"],
                planetDictTmp["Temperature"],
                planetDictTmp["Year_of_discovery"],
                planetDictTmp["HabitabilityZoneMin"],
                planetDictTmp["HabitabilityZoneMax"],
            )
            if planetLink.starName not in planetDict:
                planetDict[planetLink.starName] = []
            planetDict[planetLink.starName].append(planet)

        return (result, planetDict)

    def __createLocalization(self, location: dict) -> DH.Location:
        return DH.Location(
            location["Right_ascension"],
            location["Declination"],
            location["Parallax"],
            location["Sun_distance"],
            location["Constelation"],
        )

    def __createStars(self, stars: List[dict], planetDict: dict) -> List[DH.Star]:
        starStructList = []
        for star in stars:
            starStruct = DH.Star(
                star["Name"],
                star["Type"],
                star["Subtype"],
                star["Spectral_class"],
                star["Distance_from_the_primary"],
                star["Mass"],
                star["Size"],
                star["Temperature"],
                star["Age"],
                star["Luminosity"],
                star["Apparent_magnitude"],
                star["Absolute_magnitude"],
                star["K"],
                star["H"],
                star["J"],
                star["Grp"],
                star["I"],
                star["G"],
                star["V"],
                star["Gbp"],
                star["B"],
                star["U"],
                planetDict[star["Name"]] if star["Name"] in planetDict else [],
            )
            starStructList.append(starStruct)
        return starStructList