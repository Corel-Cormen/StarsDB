import random
from .common import measure

def fetch_batch_stars(cur, star_ids):
    query = f"""
    SELECT s.id AS star_id,
           s.name AS star_name,
           ss.name AS system_name,
           c.name AS constellation,
           l.RightAscension, l.Declination, l.Parallax, l.SunDistance,
           sc.MainDistance, sc.Mass, sc.Size, sc.Temperature, sc.Age, sc.Luminosity,
           sp.ApparentMagnitude, sp.AbsoluteMagnitude,
           st.TypeName AS star_type, sst.TypeName AS star_subtype,
           p.name AS planet_name, pt.TypeName AS planet_type, ps.TypeName AS planet_subtype,
           pc.DistanceFromStar, pc.Mass AS planet_mass, pc.Size AS planet_size
    FROM Star s
    JOIN SolarSystem ss ON s.id_system = ss.id
    JOIN Location l ON l.id_system = ss.id
    JOIN Constellation c ON l.id_constellation = c.id
    JOIN StarDetails sd ON sd.id_characteristic = s.id
    JOIN StarCharacteristic sc ON sd.id_characteristic = sc.id
    JOIN StarPhotometry sp ON sd.id_photometry = sp.id
    JOIN StarType st ON sd.id_type = st.id
    JOIN StarSubtypeDetails ssd ON sd.id = ssd.star_details_id
    JOIN StarSubtype sst ON ssd.star_subtype_id = sst.id
    LEFT JOIN Planet p ON p.id_star = s.id
    LEFT JOIN PlanetType pt ON p.id_type = pt.id
    LEFT JOIN PlanetSubtype ps ON p.id_subtype = ps.id
    LEFT JOIN PlanetCharacteristic pc ON p.id_characteristic = pc.id
    WHERE s.id IN ({','.join(['%s'] * len(star_ids))});
    """
    cur.execute(query, star_ids)
    rows = cur.fetchall()

    stars = {}
    for row in rows:
        star_id = row[0]
        if star_id not in stars:
            stars[star_id] = {
                "star_name": row[1],
                "system_name": row[2],
                "constellation": row[3],
                "location": row[4:8],
                "details": row[8:16],
                "planets": []
            }
        planet_name = row[16]
        if planet_name:
            stars[star_id]["planets"].append({
                "name": planet_name,
                "type": row[17],
                "subtype": row[18],
                "distance": row[19],
                "mass": row[20],
                "size": row[21]
            })
    return stars


def select_runner(conn, db_type, target_name, n_records, batch_size=100):
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Star;")
    count = cur.fetchone()[0]

    def db_operations():
        remaining = n_records
        while remaining > 0:
            current_batch = min(batch_size, remaining)

            star_ids = random.sample(range(1, count + 1), current_batch)

            _ = fetch_batch_stars(cur, star_ids)

            remaining -= current_batch

    res = measure(db_operations, repeats=1)
    cur.close()
    return res
