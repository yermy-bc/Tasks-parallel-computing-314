import random
import threading
import time

N_TOTAL = 50_000_000
N_THREADS = 4

total_hits = 0
lock = threading.Lock()


def monte_carlo_worker_locked(iterations: int) -> None:
    global total_hits
    rand = random.random
    for _ in range(iterations):
        x = rand()
        y = rand()
        if x * x + y * y <= 1.0:
            with lock:          # <-- every single increment takes the lock
                total_hits += 1


def run_locked() -> tuple[float, float]:
    global total_hits
    total_hits = 0
    per_thread = N_TOTAL // N_THREADS
    threads = [
        threading.Thread(target=monte_carlo_worker_locked, args=(per_thread,))
        for _ in range(N_THREADS)
    ]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start
    return 4 * total_hits / N_TOTAL, elapsed


def run_single_threaded() -> tuple[float, float]:
    rand = random.random
    hits = 0
    start = time.perf_counter()
    for _ in range(N_TOTAL):
        x = rand()
        y = rand()
        if x * x + y * y <= 1.0:
            hits += 1
    elapsed = time.perf_counter() - start
    return 4 * hits / N_TOTAL, elapsed


if __name__ == "__main__":
    print(f"Part 2: {N_TOTAL:,} points\n")

    pi_locked, t_locked = run_locked()
    print(f"Locked, 4 threads:      pi ~= {pi_locked:.6f}   time = {t_locked:.2f}s")

    pi_single, t_single = run_single_threaded()
    print(f"Single-threaded for loop: pi ~= {pi_single:.6f}   time = {t_single:.2f}s")

    print(f"\nSlowdown factor (locked-threaded / single-threaded): {t_locked / t_single:.2f}x")
