import random
from .common import measure


def delete_batch_stars(cur, star_ids, db_type):
    ids_str = ','.join(['%s'] * len(star_ids))

    if db_type == "postgresql":

        cur.execute(f"""
            WITH deleted_planets AS (
                DELETE FROM Planet 
                WHERE id_star IN ({ids_str})
                RETURNING id_characteristic
            )
            DELETE FROM PlanetCharacteristic 
            WHERE id IN (SELECT id_characteristic FROM deleted_planets);
        """, star_ids)

        cur.execute(f"""
            DELETE FROM StarSubtypeDetails 
            WHERE star_details_id IN (
                SELECT id FROM StarDetails WHERE id_characteristic IN ({ids_str})
            );
        """, star_ids)

        cur.execute(f"""
            WITH deleted_details AS (
                DELETE FROM StarDetails 
                WHERE id_characteristic IN ({ids_str})
                RETURNING id_photometry
            )
            DELETE FROM StarPhotometry 
            WHERE id IN (SELECT id_photometry FROM deleted_details);
        """, star_ids)

        cur.execute(f"DELETE FROM StarCharacteristic WHERE id IN ({ids_str});", star_ids)
        cur.execute(f"DELETE FROM Star WHERE id IN ({ids_str});", star_ids)

    else:

        cur.execute(f"SELECT id_characteristic FROM Planet WHERE id_star IN ({ids_str})", star_ids)
        planet_char_rows = cur.fetchall()
        planet_char_ids = [str(r[0]) for r in planet_char_rows if r[0] is not None]

        cur.execute(f"SELECT id, id_photometry FROM StarDetails WHERE id_characteristic IN ({ids_str})", star_ids)
        details_rows = cur.fetchall()
        details_ids = [str(r[0]) for r in details_rows]
        photometry_ids = [str(r[1]) for r in details_rows if r[1] is not None]

        if details_ids:
            cur.execute(f"DELETE FROM StarSubtypeDetails WHERE star_details_id IN ({','.join(details_ids)})")

        cur.execute(f"DELETE FROM Planet WHERE id_star IN ({ids_str});", star_ids)

        if planet_char_ids:
            cur.execute(f"DELETE FROM PlanetCharacteristic WHERE id IN ({','.join(planet_char_ids)})")

        cur.execute(f"DELETE FROM StarDetails WHERE id_characteristic IN ({ids_str});", star_ids)

        if photometry_ids:
            cur.execute(f"DELETE FROM StarPhotometry WHERE id IN ({','.join(photometry_ids)})")

        cur.execute(f"DELETE FROM StarCharacteristic WHERE id IN ({ids_str});", star_ids)
        cur.execute(f"DELETE FROM Star WHERE id IN ({ids_str});", star_ids)


def delete_runner(conn, db_type, target_name, n_records, batch_size=100):
    cur = conn.cursor()
    conn.autocommit = False

    cur.execute("SELECT id FROM Star;")
    all_ids = [row[0] for row in cur.fetchall()]

    def db_operations():
        remaining = n_records
        ids_to_process = list(all_ids)

        while remaining > 0 and ids_to_process:
            current_batch_size = min(batch_size, remaining)

            if len(ids_to_process) < current_batch_size:
                star_ids = ids_to_process
                ids_to_process = []
            else:
                star_ids = ids_to_process[:current_batch_size]
                ids_to_process = ids_to_process[current_batch_size:]

            if not star_ids:
                break

            delete_batch_stars(cur, star_ids, db_type)
            remaining -= len(star_ids)

        conn.commit()

    res = measure(db_operations, repeats=1)
    cur.close()
    return res