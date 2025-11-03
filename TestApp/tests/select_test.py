from .common import measure

def fetch_star_with_planets(cur, db_type):
    order_func = "RANDOM()" if db_type == "postgresql" else "RAND()"

    # Random star
    cur.execute(f"SELECT id, name, id_system FROM Star ORDER BY {order_func} LIMIT 1;")
    star = cur.fetchone()
    if not star:
        return None
    star_id, star_name, system_id = star

    # Solar system
    cur.execute("SELECT name FROM SolarSystem WHERE id = %s;", (system_id,))
    system_name = cur.fetchone()[0]

    # Constellation via Location
    cur.execute("""
        SELECT c.name 
        FROM Location l
        JOIN Constellation c ON l.id_constellation = c.id
        WHERE l.id_system = %s;
    """, (system_id,))
    constellation = cur.fetchone()[0]

    # Location
    cur.execute("""
        SELECT RightAscension, Declination, Parallax, SunDistance 
        FROM Location 
        WHERE id_system = %s;
    """, (system_id,))
    location = cur.fetchone()

    # StarDetails
    cur.execute("SELECT id FROM StarDetails ORDER BY id LIMIT 1;")
    star_details_id = cur.fetchone()[0]

    cur.execute("""
        SELECT sc.MainDistance, sc.Mass, sc.Size, sc.Temperature, sc.Age, sc.Luminosity,
               sp.ApparentMagnitude, sp.AbsoluteMagnitude,
               st.TypeName, sst.TypeName
        FROM StarDetails sd
        JOIN StarCharacteristic sc ON sd.id_characteristic = sc.id
        JOIN StarPhotometry sp ON sd.id_photometry = sp.id
        JOIN StarType st ON sd.id_type = st.id
        JOIN StarSubtypeDetails ssd ON sd.id = ssd.star_details_id
        JOIN StarSubtype sst ON ssd.star_subtype_id = sst.id
        WHERE sd.id = %s;
    """, (star_details_id,))
    details = cur.fetchone()

    # Planets
    cur.execute("""
        SELECT p.name, pt.TypeName, ps.TypeName, pc.DistanceFromStar, pc.Mass, pc.Size
        FROM Planet p
        JOIN PlanetType pt ON p.id_type = pt.id
        JOIN PlanetSubtype ps ON p.id_subtype = ps.id
        JOIN PlanetCharacteristic pc ON p.id_characteristic = pc.id
        WHERE p.id_star = %s;
    """, (star_id,))
    planets = cur.fetchall()

    return {
        "star_name": star_name,
        "system_name": system_name,
        "constellation": constellation,
        "location": location,
        "details": details,
        "planets": planets
    }

def select_runner(conn, db_type, target_name, n_records):
    cur = conn.cursor()

    def db_operations():
        for i in range(n_records):
            _ = fetch_star_with_planets(cur, db_type)
            # if i % 500 == 0 and i > 0:
            #     print(f"✅ Odczytano {i} rekordów gwiazd...")

    res = measure(db_operations, repeats=1)

    cur.close()
    return res

