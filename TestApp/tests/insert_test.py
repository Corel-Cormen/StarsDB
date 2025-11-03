import random
import string
from .common import measure


def random_name(prefix, length=6):
    return f"{prefix}_{''.join(random.choices(string.ascii_uppercase, k=length))}"


def insert_and_get_id(cur, query, params, db_type):
    if db_type == "postgresql":
        cur.execute(query + " RETURNING id;", params)
        return cur.fetchone()[0]
    else:  # MySQL, SQLite, itp.
        cur.execute(query + ";", params)
        return cur.lastrowid


def create_fake_star_data():
    return {
        "constellation": random_name("CONST"),
        "solar_system": random_name("SYS"),
        "location": {
            "RightAscension": random.uniform(0, 360),
            "Declination": random.uniform(-90, 90),
            "Parallax": random.uniform(0, 100),
            "SunDistance": random.uniform(0, 1000),
        },
        "star": {
            "name": random_name("STAR"),
            "MainDistance": random.uniform(0.1, 10),
            "Mass": random.uniform(0.1, 100),
            "Size": random.uniform(0.1, 10),
            "Temperature": random.uniform(2000, 10000),
            "Age": random.uniform(0.1, 10),
            "Luminosity": random.uniform(0.1, 10),
            "ApparentMagnitude": random.uniform(0, 10),
            "AbsoluteMagnitude": random.uniform(0, 10),
            "StarType": random.choice(["O", "B", "A", "F", "G", "K", "M"]),
            "StarSubType": random.choice(["Ia", "Ib", "II", "III", "IV", "V"]),
        },
        "planets": [
            {
                "name": random_name("PLAN"),
                "PlanetType": random.choice(["Gas", "Rocky", "Ice"]),
                "PlanetSubtype": random.choice(["Giant", "Terrestrial", "Dwarf"]),
                "DistanseFromStar": random.uniform(0.1, 100),
                "OrbitAroundStar": random.uniform(100, 10000),
                "Eccentricity": random.random(),
                "Mass": random.uniform(0.1, 300),
                "Size": random.uniform(0.1, 50),
                "Density": random.uniform(0.1, 15),
                "YearDiscover": random.randint(1800, 2025),
            }
            for _ in range(random.randint(1, 5))
        ],
    }


def insert_star_with_planets(cur, star_data, db_type):
    # 1. Constellation
    constellation_id = insert_and_get_id(
        cur, "INSERT INTO Constellation (name) VALUES (%s)", (star_data["constellation"],), db_type
    )

    # 2. Solar System
    system_id = insert_and_get_id(
        cur, "INSERT INTO SolarSystem (name) VALUES (%s)", (star_data["solar_system"],), db_type
    )

    # 3. Location
    loc = star_data["location"]
    cur.execute(
        """
        INSERT INTO Location (id_system, RightAscension, Declination, Parallax, SunDistance, id_constellation)
        VALUES (%s, %s, %s, %s, %s, %s);
        """,
        (system_id, loc["RightAscension"], loc["Declination"], loc["Parallax"], loc["SunDistance"], constellation_id),
    )

    # 4. Star + details
    s = star_data["star"]
    star_id = insert_and_get_id(
        cur, "INSERT INTO Star (name, id_system) VALUES (%s, %s)", (s["name"], system_id), db_type
    )

    char_id = insert_and_get_id(
        cur,
        """
        INSERT INTO StarCharacteristic (MainDistance, Mass, Size, Temperature, Age, Luminosity)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (s["MainDistance"], s["Mass"], s["Size"], s["Temperature"], s["Age"], s["Luminosity"]),
        db_type,
    )

    phot_id = insert_and_get_id(
        cur,
        """
        INSERT INTO StarPhotometry (ApparentMagnitude, AbsoluteMagnitude, StellarMagnitude)
        VALUES (%s,%s,%s)
        """,
        (s["ApparentMagnitude"], s["AbsoluteMagnitude"], None),
        db_type,
    )

    type_id = insert_and_get_id(
        cur, "INSERT INTO StarType (TypeName) VALUES (%s)", (s["StarType"],), db_type
    )

    subtype_id = insert_and_get_id(
        cur, "INSERT INTO StarSubtype (TypeName) VALUES (%s)", (s["StarSubType"],), db_type
    )

    details_id = insert_and_get_id(
        cur,
        """
        INSERT INTO StarDetails (id_type, id_characteristic, id_photometry)
        VALUES (%s,%s,%s)
        """,
        (type_id, char_id, phot_id),
        db_type,
    )

    cur.execute(
        """
        INSERT INTO StarSubtypeDetails (star_details_id, star_subtype_id)
        VALUES (%s,%s);
        """,
        (details_id, subtype_id),
    )

    # 5. Planets
    for p in star_data["planets"]:
        ptype_id = insert_and_get_id(
            cur, "INSERT INTO PlanetType (TypeName) VALUES (%s)", (p["PlanetType"],), db_type
        )

        psubtype_id = insert_and_get_id(
            cur, "INSERT INTO PlanetSubtype (TypeName) VALUES (%s)", (p["PlanetSubtype"],), db_type
        )

        pchar_id = insert_and_get_id(
            cur,
            """
            INSERT INTO PlanetCharacteristic (DistanceFromStar, OrbitAroundStar, Eccentricity, Mass, Size, Density, YearDiscover, HabitabilityZone)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                p["DistanseFromStar"],
                p["OrbitAroundStar"],
                p["Eccentricity"],
                p["Mass"],
                p["Size"],
                p["Density"],
                p["YearDiscover"],
                False,
            ),
            db_type,
        )

        cur.execute(
            """
            INSERT INTO Planet (name, id_type, id_subtype, id_characteristic, id_star)
            VALUES (%s,%s,%s,%s,%s);
            """,
            (p["name"], ptype_id, psubtype_id, pchar_id, star_id),
        )

def insert_runner(conn, db_type, target_name, n_records):
    cur = conn.cursor()
    conn.autocommit = False

    all_data = [create_fake_star_data() for _ in range(n_records)]

    def db_operations():
        for star_data in all_data:
            insert_star_with_planets(cur, star_data, db_type)
        conn.commit()

    res = measure(db_operations, repeats=1)
    cur.close()
    return res
