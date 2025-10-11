import math
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
    dms = sign * (abs(d) + m / 60 + s / 3600)
    if __less(dms, -90.0) or __greater(dms, 90.0):
        dms = dms%90
    return dms

def __close(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 0.0) -> bool:
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

def __greater(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 0.0) -> bool:
    return (not __close(a, b, rel_tol, abs_tol)) and (a > b)

def __less(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 0.0) -> bool:
    return (not __close(a, b, rel_tol, abs_tol)) and (a < b)
