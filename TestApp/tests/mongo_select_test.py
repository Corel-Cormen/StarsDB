from pymongo.collection import Collection
from .common import measure


def mongo_select_runner(client, db_type, collection_name, records):
    if db_type != "mongo":
        raise ValueError("mongo_select_runner może działać tylko z MongoDB")

    collection = client[collection_name]

    def db_operations():
        cursor = collection.find().limit(records)
        return list(cursor)

    result = measure(db_operations, repeats=1)

    return {
        "avg_ms": result["avg_ms"],
        "min_ms": result.get("min_ms", 0),
        "max_ms": result.get("max_ms", 0),
        "cpu_avg": result.get("cpu_avg", 0),
        "mem_avg_mb": result.get("mem_avg_mb", 0),
        "fetched": result.get("result", records)
    }
