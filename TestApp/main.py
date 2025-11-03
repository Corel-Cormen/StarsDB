import json
import time
import importlib
from pathlib import Path
import psycopg2
import pymysql
import pymongo
from tests.common import measure, write_result_csv, restart_container, timestamp_ms
from urllib.parse import urlparse
from tests.plot_result import plot_last_run

CONFIG_DIR = Path(__file__).parent / "configs"
TESTS_MODULE = "tests"

RECORD_SIZES = [10000]
REPEATS = 1
TESTS = [
    ("insert", "insert_test", "insert_runner"),
    ("select", "select_test", "select_runner"),
    ("update", "update_test", "update_runner"),
    ("delete", "delete_test", "delete_runner"),
]

TESTS_MONGO = [
    ("insert", "mongo_insert_test", "mongo_insert_runner"),
    ("select", "mongo_select_test", "mongo_select_runner"),
    ("update", "mongo_update_test", "mongo_update_runner"),
    ("delete", "mongo_delete_test", "mongo_delete_runner"),
]


def load_config(path):
    with open(path) as f:
        return json.load(f)


def connect_db(conf):
    db_type = conf["type"]

    if db_type == "postgresql":
        return psycopg2.connect(
            host=conf["host"],
            port=conf["port"],
            user=conf["user"],
            password=conf["password"],
            dbname=conf["database"]
        )

    elif db_type == "mysql":
        url = "jdbc:mysql://localhost:3306/star_db?allowPublicKeyRetrieval=true&useSSL=false"
        if url.startswith("jdbc:"):
            url = url[len("jdbc:"):]
        parsed = urlparse(url)
        query = dict(qc.split("=") for qc in parsed.query.split("&") if "=" in qc)

        return pymysql.connect(
            host=parsed.hostname,
            port=parsed.port or 3306,
            user=conf.get("user"),
            password=conf.get("password"),
            database=parsed.path[1:],
            autocommit=False,
            ssl={"ssl": {"check_hostname": False}} if query.get("useSSL") == "true" else None
        )

    elif db_type == "mongo":
        client = pymongo.MongoClient(conf["uri"])
        return client[conf["database"]]

    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def run_for_config(conf_path, run_id):
    conf = load_config(conf_path)
    db_type = conf.get("type")
    container_name = conf.get("container_name")
    db_label = conf.get("database", conf_path.stem)

    print(f"\n==== Running for {conf_path} ({db_type}) ====")
    restart_container(container_name)

    client = connect_db(conf)

    for records in RECORD_SIZES:
        tests_to_run = TESTS_MONGO if db_type == "mongo" else TESTS
        for op_name, module_name, func_name in tests_to_run:
            print("="*60)
            print(f"▶ Running {op_name.upper()} test on {db_type} with {records} records...")

            module = importlib.import_module(f"{TESTS_MODULE}.{module_name}")
            runner = getattr(module, func_name)

            res = runner(client, db_type, "star_systems", records)

            row = {
                "timestamp": timestamp_ms(),
                "db_type": db_type,
                "db_name": db_label,
                "container_name": container_name or "",
                "operation": op_name,
                "records": records,
                "run_id": run_id,
                "avg_ms": round(res.get("avg_ms", 0), 2),
                "min_ms": round(res.get("min_ms", res.get("avg_ms", 0)), 2),
                "max_ms": round(res.get("max_ms", res.get("avg_ms", 0)), 2),
                "cpu_avg": round(res.get("cpu_avg", 0), 2),
                "mem_avg_mb": round(res.get("mem_avg_mb", 0), 2),
                "notes": ""
            }
            write_result_csv(row)

    try:
        client.close()
    except Exception as e:
        print(f"Warning: could not close connection: {e}")

    print(f"✅ Finished tests for {db_label} ({db_type})")


if __name__ == "__main__":
    global_run_id = int(time.time())

    for conf_file in CONFIG_DIR.glob("*.json"):
        run_for_config(conf_file, global_run_id)

    print("\nAll done ✅")
    plot_last_run()
