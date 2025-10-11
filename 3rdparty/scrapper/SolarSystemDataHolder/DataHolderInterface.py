from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Location:
    rightAscension: str
    declination: str
    parallax: str
    sunDistance: str
    constelation: str


@dataclass
class Planet:
    name: str
    planetType: str
    planetSubtype: str
    distanseFromStar: str
    orbitAroundStar: str
    eccentricity: str
    mass: str
    size: str
    density: str
    temperature: str
    yearDiscover: str
    habitabilityZoneMin: str
    habitabilityZoneMax: str


@dataclass
class Star:
    name: str
    starType: str
    starSubType: str
    spectralClass: str
    mainDistance: str
    mass: str
    size: str
    temperature: str
    age: str
    luminosity: str
    apperentMagnitude: str
    absoluteMagnitude: str
    photometryK: str
    photometryH: str
    photometryJ: str
    photometryGrp: str
    photometryI: str
    photometryG: str
    photometryV: str
    photometryGbp: str
    photometryB: str
    photometryU: str
    planetList: List[Planet]


@dataclass
class StarSystem:
    name: str
    location: Location
    starList: List[Star]


class DataHolderInterface(ABC):
    """Base interface for objects storing StarSystem data.
    """

    def __init__(self):
        self.starSystemList: List[StarSystem] = []

    @abstractmethod
    def saveToFile(self):
        """Saves List[StarSystem] objects data to file.
        """
        pass
