import random
import threading
import time

N_TOTAL = 50_000_000
N_THREADS = 4

total_hits = 0  # shared, unprotected counter


def monte_carlo_worker(iterations: int) -> None:
    global total_hits
    rand = random.random
    for _ in range(iterations):
        x = rand()
        y = rand()
        if x * x + y * y <= 1.0:
            total_hits += 1  # <-- UNSYNCHRONIZED read-modify-write: the bug


def run_once() -> tuple[float, float, int]:
    global total_hits
    total_hits = 0
    per_thread = N_TOTAL // N_THREADS

    threads = [
        threading.Thread(target=monte_carlo_worker, args=(per_thread,))
        for _ in range(N_THREADS)
    ]

    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start

    pi_estimate = 4 * total_hits / N_TOTAL
    return pi_estimate, elapsed, total_hits


if __name__ == "__main__":
    print(f"Part 1: {N_TOTAL:,} points across {N_THREADS} threads, UNSYNCHRONIZED counter\n")
    results = []
    for i in range(1, 6):
        pi, elapsed, hits = run_once()
        lost = (N_TOTAL // N_THREADS) * N_THREADS  # points actually thrown
        print(f"Run {i}: pi ~= {pi:.6f}   total_hits={hits:,}   time={elapsed:.2f}s")
        results.append(pi)

    print("\nSummary (5 runs):", [f"{p:.6f}" for p in results])
