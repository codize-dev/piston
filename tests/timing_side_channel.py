"""
Description
    Using high-resolution timing to measure CPU cache access latencies,
    which could theoretically reveal information about co-located
    processes through cache-based side channels

    The sandbox cannot fully prevent timing side channels as they are
    inherent to shared hardware, but this test documents the timing
    resolution available inside the sandbox

"""

import time

samples = []
for _ in range(100):
    t1 = time.perf_counter_ns()
    t2 = time.perf_counter_ns()
    if t2 > t1:
        samples.append(t2 - t1)

if samples:
    min_res = min(samples)
    avg_res = sum(samples) // len(samples)
    print(f"Timer resolution: min={min_res}ns avg={avg_res}ns")

array_size = 1024 * 1024
data = bytearray(array_size)

t1 = time.perf_counter_ns()
for i in range(0, min(array_size, 65536), 64):
    _ = data[i]
t2 = time.perf_counter_ns()
sequential_ns = t2 - t1

stride = 4096
t1 = time.perf_counter_ns()
for i in range(0, min(array_size, 65536 * stride), stride):
    if i < array_size:
        _ = data[i]
t2 = time.perf_counter_ns()
strided_ns = t2 - t1

print(f"Sequential access: {sequential_ns}ns")
print(f"Strided access: {strided_ns}ns")

try:
    with open("/proc/cpuinfo", "r") as f:
        cpuinfo = f.read(2000)
    if "tsc" in cpuinfo.lower():
        print("TSC available in CPU flags")
except (FileNotFoundError, PermissionError):
    pass
