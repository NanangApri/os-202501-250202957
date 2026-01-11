import os
import time

print(f"Process ID: {os.getpid()}")
print("Pengujian alokasi memori Docker.... \n", flush=True)

buffer = []

def get_real_memory_mb():
    try:
        with open("/sys/fs/cgroup/memory.current", "r") as f:
            return int(f.read()) // (1024 * 1024)
    except:
        return -1

while True:
    buffer.append("M" * 10_000_000)  # ±10 MB
    real_mb = get_real_memory_mb()
    print(f"Memori aktual container: {real_mb} MB", flush=True)
    time.sleep(0.5)
