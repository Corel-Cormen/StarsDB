import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom

import StarCalculator.StarCalculator as StarCalculator
from SolarSystemDataHolder.DataHolderInterface import DataHolderInterface


class StellarcatalogDataHolder(DataHolderInterface):

    def __init__(self):
        super().__init__()

    def saveToFile(self) -> None:
        root = ET.Element("StarSystems")
        for system in self.starSystemList:
            SystemLeaf = ET.SubElement(root, "StarSystem")
            SystemLeaf.set("Name", system.name)

            locationLeaf = ET.SubElement(SystemLeaf, "Location")
            locationLeaf.set("RightAscension", str(system.location.rightAscension))
            locationLeaf.set("RightAscensionNum", str(StarCalculator.convertHMS(system.location.rightAscension)))
            locationLeaf.set("Declination", str(system.location.declination))
            locationLeaf.set("DeclinationNum", str(StarCalculator.covertDMS(system.location.declination)))
            locationLeaf.set("Parallax", str(system.location.parallax))
            locationLeaf.set("SunDistance", str(system.location.sunDistance))
            locationLeaf.set("Constelation", str(system.location.constelation))

            for star in system.starList:
                starLeaf = ET.SubElement(SystemLeaf, "Star")
                starLeaf.set("Name", str(star.name))
                starLeaf.set("StarType", str(star.starType))
                starLeaf.set("StarSubType", str(star.starSubType))
                starLeaf.set("SpectralClass", str(star.spectralClass))
                starLeaf.set("MainDistance", str(star.mainDistance))
                starLeaf.set("Mass", str(star.mass))
                starLeaf.set("Size", str(star.size))
                starLeaf.set("Temperature", str(star.temperature))
                starLeaf.set("Age", str(star.age))
                starLeaf.set("Luminosity", str(star.luminosity))
                starLeaf.set("ApperentMagnitude", str(star.apperentMagnitude))
                starLeaf.set("AbsoluteMagnitude", str(star.absoluteMagnitude))
                starLeaf.set("PhotometryK", str(star.photometryK))
                starLeaf.set("PhotometryH", str(star.photometryH))
                starLeaf.set("PhotometryJ", str(star.photometryJ))
                starLeaf.set("PhotometryGrp", str(star.photometryGrp))
                starLeaf.set("PhotometryI", str(star.photometryI))
                starLeaf.set("PhotometryG", str(star.photometryG))
                starLeaf.set("PhotometryV", str(star.photometryV))
                starLeaf.set("PhotometryGbp", str(star.photometryGbp))
                starLeaf.set("PhotometryB", str(star.photometryB))
                starLeaf.set("PhotometryU", str(star.photometryU))

                for planet in star.planetList:
                    planetLeaf = ET.SubElement(starLeaf, "Planet")
                    planetLeaf.set("Name", str(planet.name))
                    planetLeaf.set("PlanetType", str(planet.planetType))
                    planetLeaf.set("PlanetSubtype", str(planet.planetSubtype))
                    planetLeaf.set("DistanseFromStar", str(planet.distanseFromStar))
                    planetLeaf.set("OrbitAroundStar", str(planet.orbitAroundStar))
                    planetLeaf.set("Eccentricity", str(planet.eccentricity))
                    planetLeaf.set("Mass", str(planet.mass))
                    planetLeaf.set("Size", str(planet.size))
                    planetLeaf.set("Density", str(planet.density))
                    planetLeaf.set("Temperature", str(planet.temperature))
                    planetLeaf.set("YearDiscover", str(planet.yearDiscover))
                    planetLeaf.set("HabitabilityZoneMin", str(planet.habitabilityZoneMin))
                    planetLeaf.set("HabitabilityZoneMax", str(planet.habitabilityZoneMax))

        xml_str = ET.tostring(root, encoding="utf-8")
        parsed = minidom.parseString(xml_str)
        pretty_xml = parsed.toprettyxml(indent="\t")

        fileName = datetime.now().strftime("ScrapData_%Y_%m_%d_%H_%M_%S.xml")
        with open(fileName, "w", encoding="utf-8") as f:
            f.write(pretty_xml)
            print(f"Data save to {fileName} finsih")
