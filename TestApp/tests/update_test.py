import random
from .common import measure

def update_random_star(cur, db_type):
    order_func = "RANDOM()" if db_type == "postgresql" else "RAND()"
    cur.execute(f"SELECT id FROM Star ORDER BY {order_func} LIMIT 1;")
    row = cur.fetchone()
    if not row:
        return
    star_id = row[0]

    cur.execute("""
        SELECT sd.id_characteristic
        FROM StarDetails sd
        JOIN StarSubtypeDetails ssd ON sd.id = ssd.star_details_id
        LIMIT 1;
    """)
    char_row = cur.fetchone()
    if not char_row:
        return
    char_id = char_row[0]

    new_temp = random.uniform(2000, 12000)
    new_mass = random.uniform(0.1, 200)
    new_size = random.uniform(0.1, 20)

    cur.execute("""
        UPDATE StarCharacteristic
        SET Temperature = %s, Mass = %s, Size = %s
        WHERE id = %s;
    """, (new_temp, new_mass, new_size, char_id))

def update_runner(conn, db_type, target_name, n_records):
    cur = conn.cursor()
    conn.autocommit = False

    def db_operations():
        for i in range(n_records):
            update_random_star(cur, db_type)
        conn.commit()

    res = measure(db_operations, repeats=1)
    cur.close()
    return res
