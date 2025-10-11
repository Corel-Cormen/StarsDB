import re
from astropy.coordinates import SkyCoord
from astropy import units as u


def calcConstellation(ra: str|float, dec: str|float) -> str:
    if type(ra) == str and type(dec) == str:
        __ra = convertHMS(ra)
        __dec = covertDMS(dec)
    else:
        __ra = ra
        __dec = dec
    return SkyCoord(ra=__ra*u.deg, dec=__dec*u.deg, frame='icrs').get_constellation()

def convertHMS(ra: str) -> float:
    match = re.match(r"([+-]?\d+)h\s*([+-]?\d+)m\s*([+-]?[\d.]+)s", ra)
    if not match:
        raise ValueError(f"Incorrect format RA: {ra}")
    h, m, s = map(float, match.groups())
    return (h + (m / 60) + (s / 3600)) * 15

def covertDMS(dec) -> float:
    match = re.match(r"([+-]?\d+)°\s*(\d+)'?\s*([\d.]+)\"?", dec.replace("''", '"'))
    if not match:
        raise ValueError(f"Incorrect format Dec: {dec}")
    d, m, s = map(float, match.groups())
    sign = 1 if d >= 0 else -1
    if (-90.0 > d) or (d > 90.0):
        d = d%90
    return sign * (abs(d) + m / 60 + s / 3600)
