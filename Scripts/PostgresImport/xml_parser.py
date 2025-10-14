import xml.etree.ElementTree as ET

def _to_none_or(value, cast=None):
    if value is None:
        return None
    v = value.strip()
    if v == "":
        return None
    v = v.replace(',', '')
    if cast:
        try:
            return cast(v)
        except Exception:
            return None
    return v

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    systems = []
    for system in root.findall('StarSystem'):
        system_name = _to_none_or(system.get('Name'))
        loc = system.find('Location')
        location = None
        if loc is not None:
            location = {
                "RightAscension": _to_none_or(loc.get('RightAscension')),
                "RightAscensionNum": _to_none_or(loc.get('RightAscensionNum'), float),
                "Declination": _to_none_or(loc.get('Declination')),
                "DeclinationNum": _to_none_or(loc.get('DeclinationNum'), float),
                "Parallax": _to_none_or(loc.get('Parallax'), float),
                "SunDistance": _to_none_or(loc.get('SunDistance'), float),
                "Constelation": _to_none_or(loc.get('Constelation'))
            }

        stars = []
        for star in system.findall('Star'):
            star_data = {
                "Name": _to_none_or(star.get('Name')),
                "StarType": _to_none_or(star.get('StarType')),
                "StarSubType": _to_none_or(star.get('StarSubType')),
                "SpectralClass": _to_none_or(star.get('SpectralClass')),
                "Mass": _to_none_or(star.get('Mass'), float),
                "Size": _to_none_or(star.get('Size'), float),
                "Temperature": _to_none_or(star.get('Temperature'), float),
                "Age": _to_none_or(star.get('Age'), float),
                "Luminosity": _to_none_or(star.get('Luminosity'), float),
                "ApperentMagnitude": _to_none_or(star.get('ApperentMagnitude'), float),
                "AbsoluteMagnitude": _to_none_or(star.get('AbsoluteMagnitude'), float),
                "PhotometryK": _to_none_or(star.get('PhotometryK'), float),
                "PhotometryH": _to_none_or(star.get('PhotometryH'), float),
                "PhotometryJ": _to_none_or(star.get('PhotometryJ'), float),
                "PhotometryGrp": _to_none_or(star.get('PhotometryGrp'), float),
                "PhotometryI": _to_none_or(star.get('PhotometryI'), float),
                "PhotometryG": _to_none_or(star.get('PhotometryG'), float),
                "PhotometryV": _to_none_or(star.get('PhotometryV'), float),
                "PhotometryGbp": _to_none_or(star.get('PhotometryGbp'), float),
                "PhotometryB": _to_none_or(star.get('PhotometryB'), float),
                "PhotometryU": _to_none_or(star.get('PhotometryU'), float),
            }

            planets = []
            for planet in star.findall('Planet'):
                p = {k: _to_none_or(planet.get(k)) for k in planet.keys()}
                for key in ("DistanseFromStar", "OrbitAroundStar", "Eccentricity", "Mass", "Size", "Density", "Temperature"):
                    if p.get(key) is not None:
                        try:
                            p[key] = float(p[key].replace(',', ''))
                        except Exception:
                            try:
                                p[key] = float(p[key].split()[0])
                            except Exception:
                                p[key] = None
                if p.get("YearDiscover"):
                    try:
                        p["YearDiscover"] = int(p["YearDiscover"])
                    except Exception:
                        p["YearDiscover"] = None
                planets.append(p)

            star_data["Planets"] = planets
            stars.append(star_data)

        systems.append({
            "Name": system_name,
            "Location": location,
            "Stars": stars
        })

    return systems
