import random
from .common import measure

def update_batch_stars(cur, star_char_ids):
    updates = []
    for char_id in star_char_ids:
        new_temp = random.uniform(2000, 12000)
        new_mass = random.uniform(0.1, 200)
        new_size = random.uniform(0.1, 20)
        updates.append((char_id, new_temp, new_mass, new_size))

    query = f"""
    UPDATE StarCharacteristic
    SET Temperature = CASE id
        {''.join([f'WHEN {u[0]} THEN {u[1]} ' for u in updates])}
        END,
        Mass = CASE id
        {''.join([f'WHEN {u[0]} THEN {u[2]} ' for u in updates])}
        END,
        Size = CASE id
        {''.join([f'WHEN {u[0]} THEN {u[3]} ' for u in updates])}
        END
    WHERE id IN ({','.join([str(u[0]) for u in updates])});
    """
    cur.execute(query)


def update_runner(conn, db_type, target_name, n_records, batch_size=100):
    cur = conn.cursor()

    if db_type != "postgresql":
        conn.autocommit = False

    cur.execute("SELECT id FROM StarCharacteristic;")
    all_ids = [row[0] for row in cur.fetchall()]

    def db_operations():
        remaining = n_records
        while remaining > 0:
            current_batch = min(batch_size, remaining)
            star_char_ids = random.sample(all_ids, current_batch)
            update_batch_stars(cur, star_char_ids)
            remaining -= current_batch

        conn.commit()

    res = measure(db_operations, repeats=1)
    cur.close()
    return res
