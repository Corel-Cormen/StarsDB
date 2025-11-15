import random
from .common import measure

def delete_batch_stars(cur, star_ids, db_type):
    ids_str = ','.join(['%s'] * len(star_ids))

    if db_type == "postgresql":
        cur.execute(f"DELETE FROM Planet WHERE id_star IN ({ids_str});", star_ids)

        cur.execute(f"""
            DELETE FROM PlanetCharacteristic pc
            USING Planet p
            WHERE pc.id = p.id_characteristic AND p.id_star IN ({ids_str});
        """, star_ids)

        cur.execute(f"""
            DELETE FROM StarSubtypeDetails ssd
            USING StarDetails sd
            WHERE ssd.star_details_id = sd.id AND sd.id_characteristic IN ({ids_str});
        """, star_ids)

        cur.execute(f"DELETE FROM StarDetails WHERE id_characteristic IN ({ids_str});", star_ids)

        cur.execute(f"""
            DELETE FROM StarPhotometry sp
            USING StarDetails sd
            WHERE sp.id = sd.id_photometry AND sd.id_characteristic IN ({ids_str});
        """, star_ids)

        cur.execute(f"""
            DELETE FROM StarCharacteristic sc
            WHERE sc.id IN ({ids_str});
        """, star_ids)

        cur.execute(f"DELETE FROM Star WHERE id IN ({ids_str});", star_ids)

    else:
        cur.execute(f"""
            DELETE ssd FROM StarSubtypeDetails ssd
            JOIN StarDetails sd ON ssd.star_details_id = sd.id
            WHERE sd.id_characteristic IN ({ids_str});
        """, star_ids)

        cur.execute(f"DELETE FROM StarDetails WHERE id_characteristic IN ({ids_str});", star_ids)

        cur.execute(f"""
            DELETE sp FROM StarPhotometry sp
            JOIN StarDetails sd ON sp.id = sd.id_photometry
            WHERE sd.id_characteristic IN ({ids_str});
        """, star_ids)

        cur.execute(f"""
            DELETE sc FROM StarCharacteristic sc
            WHERE sc.id IN ({ids_str});
        """, star_ids)

        cur.execute(f"DELETE FROM Planet WHERE id_star IN ({ids_str});", star_ids)

        cur.execute(f"""
            DELETE pc FROM PlanetCharacteristic pc
            JOIN Planet p ON pc.id = p.id_characteristic
            WHERE p.id_star IN ({ids_str});
        """, star_ids)

        cur.execute(f"DELETE FROM Star WHERE id IN ({ids_str});", star_ids)


def delete_runner(conn, db_type, target_name, n_records, batch_size=100):
    cur = conn.cursor()
    conn.autocommit = False

    cur.execute("SELECT id FROM Star;")
    all_ids = [row[0] for row in cur.fetchall()]

    def db_operations():
        remaining = n_records
        while remaining > 0:
            current_batch = min(batch_size, remaining)
            star_ids = random.sample(all_ids, current_batch)
            delete_batch_stars(cur, star_ids, db_type)
            remaining -= current_batch

        conn.commit()

    res = measure(db_operations, repeats=1)
    cur.close()
    return res
