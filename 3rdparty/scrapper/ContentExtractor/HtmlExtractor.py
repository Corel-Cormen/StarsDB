import re
from bs4 import BeautifulSoup
from typing import List, Tuple

import StarCalculator.StarCalculator as StarCalculator
from ContentExtractor.ContentExtractorInterface import ContentExtractorInterface, StarWebside


class HtmlExtractor(ContentExtractorInterface):

    def extractStarLink(self, html: str) -> List[StarWebside]:
        htmlTable = self.__extractStarsMainTable(html)
        soup = BeautifulSoup(htmlTable, "html.parser")
        stars = []

        for a in soup.find_all("a", href=True):
            if a["href"].startswith("stars/"):
                name = a.contents[0].strip()
                link = '/' + a["href"]
                stars.append(StarWebside(name, link))

        return stars

    def __extractStarsMainTable(self, html: str) -> str:
        startMarker = "<table class='starlist2'"
        endMarker = "</table>"

        pos = html.find(startMarker)
        htmlTable = html[pos:]
        pos = htmlTable.find(endMarker)
        htmlTable = htmlTable[:(pos + len(endMarker))]

        return htmlTable

    def extractPlanetLink(self, mainLink: str, html: str) -> List[StarWebside]:
        links = []

        soup = BeautifulSoup(html, "html.parser")
        starsHtmlList = soup.find_all("div", class_="starInfo")
        if self.__checkLengthHtmlTable(starsHtmlList):
            soup = BeautifulSoup(str(starsHtmlList[-1]), "html.parser")
            starName = ""
            for a in soup.find_all("a", href=True):
                planetLink = "/" + a['href']
                if (planetLink != mainLink) and (planetLink != "/stars/"):
                    links.append(StarWebside(starName, planetLink))
                else:
                    starName = a.get_text(strip=True)

        return links

    def checkContent(self, html: str) -> bool:
        soup = BeautifulSoup(html, "html.parser")
        htmlDivList = soup.find_all("div", class_="starInfo")
        return True if len(htmlDivList) else False

    def extractSystemName(self, html: str) -> str:
        prefix = "Star "
        return self.__serialzeHeader(html, prefix)

    def extractStars(self, html: str) -> Tuple[bool, dict, List[dict]]:
        soup = BeautifulSoup(html, "html.parser")
        locationDict = {}
        starDistList = []

        starsHtmlList = soup.find_all("div", class_="starInfo")
        if self.__checkLengthHtmlTable(starsHtmlList):
            starsHtmlList = starsHtmlList[:-1]

        for starHtml in starsHtmlList:
            starDict = {}

            starDict["Name"] = self.__serializeName(starHtml)
            starType, starSubtype = self.__serializeType(starHtml)
            starDict["Type"] = starType
            starDict["Subtype"] = starSubtype

            textHtml = starHtml.get_text(" ", strip=False)

            if ("Right_ascension" not in locationDict) and (textHtml.find("Right ascension: ") != -1):
                locationDict["Right_ascension"] = self.__serializeFiled(textHtml, "Right ascension")
            if ("Declination" not in locationDict) and (textHtml.find("Declination: ") != -1):
                locationDict["Declination"] = self.__serializeFiled(textHtml, "Declination", "(")
            if ("Parallax" not in locationDict) and (textHtml.find("Parallax: ") != -1):
                locationDict["Parallax"] = self.__serializeFiled(textHtml, "Parallax")
            if ("Sun_distance" not in locationDict) and (textHtml.find("Sun distance: ") != -1):
                locationDict["Sun_distance"] = self.__serializeFiled(textHtml, "Sun distance", "ly")
            if ("Right_ascension" in locationDict) and ("Declination" in locationDict):
                locationDict["Constelation"] = StarCalculator.calcConstellation(locationDict["Right_ascension"], locationDict["Declination"])

            starDict["Spectral_class"] = self.__serializeFiled(textHtml, "Spectral class")
            starDict["Distance_from_the_primary"] = self.__serializeFiled(textHtml, "Distance from the primary", "AU")
            starDict["Mass"] = self.__serializeFiled(textHtml, "Mass", "%")
            starDict["Size"] = self.__serializeFiled(textHtml, "Size", "%")
            starDict["Temperature"] = self.__serializeFiled(textHtml, "Temperature", "K")
            starDict["Age"] = self.__serializeFiled(textHtml, "Age", "billions years")
            starDict["Luminosity"] = self.__serializeFiled(textHtml, "Luminosity", "L")
            starDict["Apparent_magnitude"] = self.__serializeFiled(textHtml, "Apparent magnitude (V)")
            starDict["Absolute_magnitude"] = self.__serializeFiled(textHtml, "Absolute magnitude (V)")

            self.__serialzePhotometry(starHtml, starDict)

            starDistList.append(starDict)

        return (self.__verifyLocation(locationDict), locationDict, starDistList)

    def __verifyLocation(self, location: dict) -> bool:
        result = True
        if "Right_ascension" not in location or \
            "Declination" not in location or \
            "Parallax" not in location or \
            "Sun_distance" not in location or \
            "Constelation" not in location:
                result = False
        return result

    def extractPlanet(self, html: str) -> dict:
        planetDict = {}
        soup = BeautifulSoup(html, "html.parser")
        planetInfo = soup.find_all("div", class_="starInfo")
        planetHtml = planetInfo[0]

        planetDict["Name"] = self.__serializeName(planetHtml)
        planetType, planetSubtype = self.__serializeType(planetHtml)
        planetDict["Type"] = planetType
        planetDict["Subtype"] = planetSubtype

        textHtml = planetHtml.get_text(" ", strip=False)

        planetDict["Distance_from_the_star"] = self.__serializeFiled(textHtml, "Distance from the star", "AU")
        planetDict["Orbit_around_star"] = self.__serializeFiled(textHtml, "Orbit around star", "days")
        planetDict["Eccentricity"] = self.__serializeFiled(textHtml, "Eccentricity")

        planetDict["Mass"] = self.__serializeFiled(textHtml, "Mass", "M")
        planetDict["Size"] = self.__serializeFiled(textHtml, "Size", "R")
        planetDict["Density"] = self.__serializeFiled(textHtml, "Density", "kg/m")
        planetDict["Temperature"] = self.__serializeFiled(textHtml, "Temperature", "K")
        planetDict["Year_of_discovery"] = self.__serializeFiled(textHtml, "Year of discovery", "(")

        habitabilityMin, habitabilityMax = self.__serializeHabitability(planetInfo)
        planetDict["HabitabilityZoneMin"] = habitabilityMin
        planetDict["HabitabilityZoneMax"] = habitabilityMax

        return planetDict

    def __serialzeHeader(self, html: str, prefix: str) -> str:
        systemName = ""
        soup = BeautifulSoup(html, "html.parser")
        mainBox = soup.find("div", class_="mainBox")

        if mainBox:
            h1 = mainBox.find("h1")
            if h1:
                systemName: str = h1.text.strip()
                if systemName.startswith(prefix):
                    systemName = systemName[len(prefix):]

        return systemName

    def __serializeName(self, htmlObj) -> str:
        result = ""
        titleHtml = htmlObj.find("h2", class_="title")
        if titleHtml:
            result = titleHtml.text.strip()
        return result

    def __serializeType(self, html: BeautifulSoup) -> tuple[str, str]:
        outStarType = ""
        outStatSubtype = ""

        starTypeHtml = html.find("div", class_="noteBig")
        if starTypeHtml:
            starTypes = starTypeHtml.text.strip().split(',', 1)
            outStarType = starTypes[0]
            if len(starTypes) > 1:
                subtypes = ""
                for t in starTypes[1].split(','):
                    if len(t.strip()):
                        subtypes += (t.strip() + ", ")
                    outStatSubtype = subtypes[:-2]

        return (outStarType, outStatSubtype)

    def __serialzePhotometry(self, html: BeautifulSoup, starDict: dict):
        fieldList = [
            "K", "H", "J", "Grp", "I",
            "G", "V", "Gbp", "B", "U",
        ]
        fieldAssignIdx = 0

        for graphCol in html.find_all("div", class_="graphColCont"):
            graph = graphCol.find("div", class_="graphCol")
            if graph:
                style = graph.get("style", "")
                if "height:" in style:
                    if "px" in style:
                        blockHightPx = float(style.split("height:")[1].split("px")[0].strip())
                        magnitudo = 5 * (blockHightPx/65.0)
                        starDict[fieldList[fieldAssignIdx]] = str(magnitudo)
                        fieldAssignIdx += 1
                    else:
                        starDict[fieldList[fieldAssignIdx]] = "0.0"
                        fieldAssignIdx += 1
                else:
                    print("Not found height style")
            else:
                print("Not found graphCol div")

        for field in fieldList:
            if field not in starDict:
                print("Detect invalid Photometry chart")
                for f in fieldList:
                    starDict[f] = ""
                break

    def __serializeHabitability(self, html: BeautifulSoup) -> tuple[str, str]:
        habitabilityMin = ""
        habitabilityMax = ""

        if(len(html) == 4):
            habitabilityHtml = html[3].get_text(" ", strip=False)
            habitability = self.__serializeFiled(habitabilityHtml, "Habitable zone of the star", "AU")
            habitabilityField = habitability.split('-')
            habitabilityMin = habitabilityField[0]
            habitabilityMax = habitabilityField[1]

        return (habitabilityMin, habitabilityMax)

    def __serializeFiled(self, html: str, filed: str, unit: str = ''):
        result = ""
        data = self.__extractFiled(html, filed)
        if len(unit):
            result = data.split(unit, 1)[0].strip()
        else:
            result = data.strip()
        return result

    def __extractFiled(self, text: str, filed: str) -> str:
        result = ""
        if text.find(filed + ": ") != -1:
            match = re.search(rf"{re.escape(filed)}:\s*(.*?)\s*\n", text)
            if match:
                result = match.group(1)
        return result

    def __checkLengthHtmlTable(self, HtmlTable: BeautifulSoup) -> bool:
        return "system structure" in str(HtmlTable[-1].find("h2", class_="title small"))
