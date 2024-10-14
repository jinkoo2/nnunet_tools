import os

# Get memory info from /proc/meminfo (Linux only)
with open("/proc/meminfo") as f:
    meminfo = f.readlines()

mem_total = int([x for x in meminfo if "MemTotal" in x][0].split()[1])  # kB
mem_free = int([x for x in meminfo if "MemAvailable" in x][0].split()[1])  # kB

print(f"Total Memory: {mem_total / 1024 / 1024:.2f} GB")
print(f"Available Memory: {mem_free / 1024 / 1024:.2f} GB")
