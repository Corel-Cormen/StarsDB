import sys
from config import get_connection
from xml_parser import parse_xml

BATCH_SIZE = 5000

def insert_constellation(cursor, name):
    cursor.execute("INSERT INTO Constellation (name) VALUES (%s);", (name,))
    return cursor.lastrowid

def insert_solar_system(cursor, name):
    cursor.execute("INSERT INTO SolarSystem (name) VALUES (%s);", (name,))
    return cursor.lastrowid

def insert_location(cursor, system_id, loc, constellation_id):
    cursor.execute("""
        INSERT INTO Location (id_system, RightAscension, Declination, Parallax, SunDistance, id_constellation)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (system_id, loc.get("RightAscensionNum"), loc.get("DeclinationNum"),
          loc.get("Parallax"), loc.get("SunDistance"), constellation_id))

def insert_star(cursor, name, system_id):
    cursor.execute("INSERT INTO Star (name, id_system) VALUES (%s, %s);", (name, system_id))
    return cursor.lastrowid

def insert_star_characteristic(cursor, star):
    cursor.execute("""
        INSERT INTO StarCharacteristic (MainDistance, Mass, Size, Temperature, Age, Luminosity)
        VALUES (%s,%s,%s,%s,%s,%s);
    """, (star.get('MainDistance'), star.get('Mass'), star.get('Size'),
          star.get('Temperature'), star.get('Age'), star.get('Luminosity')))
    return cursor.lastrowid

def insert_star_photometry(cursor, star):
    cursor.execute("""
        INSERT INTO StarPhotometry (ApparentMagnitude, AbsoluteMagnitude, StellarMagnitude)
        VALUES (%s,%s,%s);
    """, (star.get('ApperentMagnitude'), star.get('AbsoluteMagnitude'), None))
    return cursor.lastrowid

def insert_star_type(cursor, name):
    cursor.execute("INSERT INTO StarType (TypeName) VALUES (%s);", (name,))
    return cursor.lastrowid

def insert_star_subtype(cursor, name):
    cursor.execute("INSERT INTO StarSubtype (TypeName) VALUES (%s);", (name,))
    return cursor.lastrowid

def insert_star_details(cursor, type_id, char_id, phot_id):
    cursor.execute("""
        INSERT INTO StarDetails (id_type, id_characteristic, id_photometry)
        VALUES (%s,%s,%s);
    """, (type_id, char_id, phot_id))
    return cursor.lastrowid

def insert_star_subtype_details(cursor, details_id, subtype_id):
    cursor.execute("""
        INSERT INTO StarSubtypeDetails (star_details_id, star_subtype_id)
        VALUES (%s,%s);
    """, (details_id, subtype_id))

def insert_planet_type(cursor, name):
    cursor.execute("INSERT INTO PlanetType (TypeName) VALUES (%s);", (name,))
    return cursor.lastrowid

def insert_planet_subtype(cursor, name):
    cursor.execute("INSERT INTO PlanetSubtype (TypeName) VALUES (%s);", (name,))
    return cursor.lastrowid

def insert_planet_characteristics(cursor, p):
    cursor.execute("""
        INSERT INTO PlanetCharacteristic (DistanceFromStar, OrbitAroundStar, Eccentricity, Mass, Size, Density, YearDiscover, HabitabilityZone)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
    """, (p.get('DistanseFromStar'), p.get('OrbitAroundStar'), p.get('Eccentricity'),
          p.get('Mass'), p.get('Size'), p.get('Density'), p.get('YearDiscover'), False))
    return cursor.lastrowid

def insert_planet(cursor, name, type_id, subtype_id, char_id, star_id):
    cursor.execute("""
        INSERT INTO Planet (name, id_type, id_subtype, id_characteristic, id_star)
        VALUES (%s,%s,%s,%s,%s);
    """, (name, type_id, subtype_id, char_id, star_id))

def import_file(xml_path):
    print(f"⏳ Parsowanie XML: {xml_path}")
    systems = parse_xml(xml_path)
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    inserted = 0
    try:
        for system in systems:
            system_id = insert_solar_system(cur, system["Name"])
            constellation_id = None

            if system["Location"]:
                constellation_id = insert_constellation(cur, system["Location"]["Constelation"])
                insert_location(cur, system_id, system["Location"], constellation_id)

            for star in system["Stars"]:
                star_id = insert_star(cur, star["Name"], system_id)
                char_id = insert_star_characteristic(cur, star)
                phot_id = insert_star_photometry(cur, star)
                type_id = insert_star_type(cur, star.get("StarType"))
                subtype_id = insert_star_subtype(cur, star.get("StarSubType"))
                details_id = insert_star_details(cur, type_id, char_id, phot_id)
                insert_star_subtype_details(cur, details_id, subtype_id)

                for planet in star["Planets"]:
                    ptype_id = insert_planet_type(cur, planet.get("PlanetType"))
                    psubtype_id = insert_planet_subtype(cur, planet.get("PlanetSubtype"))
                    pchar_id = insert_planet_characteristics(cur, planet)
                    insert_planet(cur, planet.get("Name"), ptype_id, psubtype_id, pchar_id, star_id)

                inserted += 1
                if inserted % BATCH_SIZE == 0:
                    conn.commit()
                    print(f"✅ Wstawiono {inserted} gwiazd (plus powiązania)")

        conn.commit()
        print(f"🎉 Zakończono import — wstawiono {inserted} gwiazd.")
    except Exception as e:
        conn.rollback()
        print("❌ Błąd:", e)
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python import_xml_to_db.py <plik.xml>")
        sys.exit(1)
    import_file(sys.argv[1])
