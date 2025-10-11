import json
import os.path
import random
from dataclasses import dataclass
from typing import List

from Scrapper.ScrapperInterface import ScrapperInterface
import StarCalculator.StarCalculator as sc
import SolarSystemDataHolder.DataHolderInterface as DH


class GeneratorScrapper(ScrapperInterface):

    @dataclass
    class GenCfg:
        systemQuantity: int = 0
        maxStarQuantity: int = 0
        maxPlanetQuantity: int = 0

    def scrap(self, dataHolder: DH.DataHolderInterface) -> bool:
        result = True
        if os.path.isfile(".genCfg"):
            print("Detect generate config file.")
            cfg = self.__loadCfg()

            for systemNum in range(1, cfg.systemQuantity+1):
                systemName = f"Gen_System_{systemNum}"
                location = self.__genLocation()
                starList = self.__genStars(systemName, cfg.maxStarQuantity)
                for idx in range(len(starList)):
                    starList[idx].planetList = self.__genPlanets(starList[idx].name, cfg.maxPlanetQuantity)
                system = DH.StarSystem(systemName,
                                       location,
                                       starList,
                                       )
                dataHolder.starSystemList.append(system)

        else:
            print("No detect generate config file.")
            result = False

        return result

    def __loadCfg(self) -> GenCfg:
        cfg = self.GenCfg
        with open(".genCfg.json", "r", encoding="utf-8") as cfgFile:
            jsonCfg = json.load(cfgFile)
            cfg.systemQuantity = jsonCfg["SystemQuantity"]
            cfg.maxStarQuantity = jsonCfg["MaxStarQuantity"]
            cfg.maxPlanetQuantity = jsonCfg["MaxPlanetQuantity"]
        return cfg

    def __genLocation(self) -> DH.Location:
        PC2LY = 3.26156

        right_ascension = f"{random.randint(0, 23)}h {random.randint(0, 59)}m {random.random() * 59:.3f}s"
        declination = f"{random.randint(0, 359)}° {random.randint(0, 59)}' {random.random() * 59:.3f}''"
        parallax = random.uniform(0.1, 1000)
        sunDistance = (1000/parallax) * PC2LY

        return DH.Location(right_ascension,
                           declination,
                           str(parallax),
                           str(sunDistance),
                           sc.calcConstellation(right_ascension, declination)
                           )

    def __genStars(self, systemName: str, starQuantity: int) -> List[DH.Star]:
        starsList = []
        randStarsQuantity = random.randint(1, starQuantity)
        for idx in range(1, randStarsQuantity+1):
            starsList.append(DH.Star(
                f"{systemName}_Gen_Star_{idx}",
                "TO DO",
                "TO DO",
                "TO DO",
                str(random.uniform(1.0, 100.0)),
                str(random.uniform(0.1, 100.0)),
                str(random.uniform(0.1, 100.0)),
                str(random.randint(1000, 10000)),
                str(random.uniform(0.1, 15.0)),
                str(random.uniform(0.1, 10.0)),
                str(random.uniform(-10.0, 10.0)),
                str(random.uniform(-10.0, 10.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                str(random.uniform(0.0, 5.0)),
                []
            ))
        return starsList

    def __genPlanets(self, starName: str, planetQuantity) -> List[DH.Planet]:
        planetList = []
        randPlanetQuantity = random.randint(0, planetQuantity)
        for idx in range(1, randPlanetQuantity+1):
            planetList.append(DH.Planet(
                f"{starName}_Gen_Planet{idx}",
                "TO DO",
                "TO DO",
                str(random.uniform(0.1, 20.0)),
                str(random.uniform(0.1, 20.0)),
                str(random.uniform(0.0, 1.0)),
                str(random.uniform(0.1, 20.0)),
                str(random.uniform(0.1, 20.0)),
                str(random.randint(500, 5000)),
                str(random.randint(-270, 1000)),
                str(random.randint(2015, 2025)),
                str(random.uniform(0.0, 100.0)),
                str(random.uniform(0.0, 100.0))
            ))
        return planetList
