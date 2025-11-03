from datetime import datetime
import random
from .common import measure


def generate_star_document(i):
    return {
        "Name": f"System_{i}_{datetime.utcnow().timestamp()}",
        "Location": {
            "RightAscensionNum": random.uniform(0, 360),
            "DeclinationNum": random.uniform(-90, 90),
            "SunDistance": random.uniform(0, 10000),
        },
        "Stars": [
            {
                "Name": f"Star_{i}",
                "StarType": random.choice(["G", "K", "M", "F", "A"]),
                "Mass": random.uniform(0.1, 10),
                "Temperature": random.uniform(3000, 10000),
                "Planets": [
                    {
                        "Name": f"Planet_{i}_{j}",
                        "Mass": random.uniform(0.1, 300),
                        "Size": random.uniform(1000, 50000),
                    }
                    for j in range(random.randint(1, 5))
                ],
            }
        ],
        "CreatedAt": datetime.utcnow(),
    }


def mongo_insert_runner(client, db_type, collection_name, records):
    if db_type != "mongo":
        raise ValueError("mongo_insert_runner może działać tylko z MongoDB")

    db = client
    collection = db["star_systems"]

    docs = [generate_star_document(i) for i in range(records)]

    def db_operations():
        collection.insert_many(docs)

    result = measure(db_operations, repeats=1)
    return {
        "avg_ms": result["avg_ms"],
        "min_ms": result.get("min_ms", 0),
        "max_ms": result.get("max_ms", 0),
        "cpu_avg": result.get("cpu_avg", 0),
        "mem_avg_mb": result.get("mem_avg_mb", 0),
        "fetched": result.get("result", records)
    }
