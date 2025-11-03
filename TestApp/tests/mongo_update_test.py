from pymongo import UpdateOne
from .common import measure


def mongo_update_runner(db, db_type, collection_name, records):
    if "mongo" not in db_type:
        raise ValueError("mongo_update_runner może działać tylko z MongoDB")

    collection = db[collection_name]

    cursor = collection.find({}, {"_id": 1}).limit(records)
    updates = [
        UpdateOne(
            {"_id": doc["_id"]},
            {"$set": {"Location.Constellation": "UpdatedConstellation"}}
        )
        for doc in cursor
    ]

    def db_operations():
        if updates:
            collection.bulk_write(updates)

    result = measure(db_operations, repeats=1)

    return {
        "avg_ms": result["avg_ms"],
        "min_ms": result.get("min_ms", 0),
        "max_ms": result.get("max_ms", 0),
        "cpu_avg": result.get("cpu_avg", 0),
        "mem_avg_mb": result.get("mem_avg_mb", 0),
        "fetched": result.get("result", records)
    }
