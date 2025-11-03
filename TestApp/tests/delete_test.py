import random
from .common import measure

def delete_random_star(cur, db_type):
    order_func = "RANDOM()" if db_type == "postgresql" else "RAND()"
    cur.execute(f"SELECT id FROM Star ORDER BY {order_func} LIMIT 1;")
    row = cur.fetchone()
    if not row:
        return
    star_id = row[0]

    cur.execute("SELECT id, id_characteristic FROM Planet WHERE id_star = %s;", (star_id,))
    planets = cur.fetchall()
    for p_id, p_char_id in planets:
        cur.execute("DELETE FROM Planet WHERE id = %s;", (p_id,))
        cur.execute("DELETE FROM PlanetCharacteristic WHERE id = %s;", (p_char_id,))

    cur.execute("""
        SELECT sd.id, sd.id_characteristic, sd.id_photometry
        FROM StarDetails sd
        JOIN StarSubtypeDetails ssd ON sd.id = ssd.star_details_id
        LIMIT 1;
    """)
    sd_row = cur.fetchone()
    sd_id = char_id = phot_id = None
    if sd_row:
        sd_id, char_id, phot_id = sd_row

    if sd_id:
        cur.execute("DELETE FROM StarSubtypeDetails WHERE star_details_id = %s;", (sd_id,))
        cur.execute("DELETE FROM StarDetails WHERE id = %s;", (sd_id,))
    if char_id:
        cur.execute("DELETE FROM StarCharacteristic WHERE id = %s;", (char_id,))
    if phot_id:
        cur.execute("DELETE FROM StarPhotometry WHERE id = %s;", (phot_id,))

    cur.execute("DELETE FROM Star WHERE id = %s;", (star_id,))

def delete_runner(conn, db_type, target_name, n_records):
    cur = conn.cursor()
    conn.autocommit = False

    def db_operations():
        for _ in range(n_records):
            delete_random_star(cur, db_type)
        conn.commit()

    res = measure(db_operations, repeats=1)

    cur.close()
    return res
