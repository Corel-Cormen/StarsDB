import time
import csv
import os
import psutil
import subprocess
from datetime import datetime
from pathlib import Path
import statistics
import json

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RESULTS_DIR.mkdir(exist_ok=True)

def timestamp_ms():
    return int(time.time() * 1000)

def measure(func, *args, repeats=3, **kwargs):
    times = []
    cpu_usages = []
    mem_usages = []
    for _ in range(repeats):
        proc = psutil.Process()
        start_cpu = psutil.cpu_percent(interval=None)
        start_mem = psutil.virtual_memory().used
        t0 = time.perf_counter()
        func(*args, **kwargs)
        t1 = time.perf_counter()
        end_cpu = psutil.cpu_percent(interval=None)
        end_mem = psutil.virtual_memory().used
        times.append((t1 - t0) * 1000.0)
        cpu_usages.append(end_cpu - start_cpu)
        mem_usages.append((end_mem - start_mem) / (1024*1024))
    return {
        "avg_ms": statistics.mean(times),
        "min_ms": min(times),
        "max_ms": max(times),
        "cpu_avg": statistics.mean(cpu_usages),
        "mem_avg_mb": statistics.mean(mem_usages)
    }

def write_result_csv(row: dict, filename="benchmark_results.csv"):
    path = RESULTS_DIR / filename
    header = [
        "timestamp","db_type","db_name","container_name","operation",
        "records","run_id","avg_ms","min_ms","max_ms","cpu_avg","mem_avg_mb","notes"
    ]
    exists = path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in header})

def restart_container(container_name):
    if not container_name:
        return
    try:
        subprocess.run(["docker","restart",container_name], check=True)
        time.sleep(2)
    except Exception as e:
        print(f"Warning: failed to restart container {container_name}: {e}")
