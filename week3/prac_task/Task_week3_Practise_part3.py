import argparse
import math
import multiprocessing as mp
import random
import time


def worker_chunk(iterations: int, seed: int) -> int:
    """Each process: purely local accumulation, no shared state at all."""
    rng = random.Random(seed)
    rand = rng.random
    local_hits = 0
    for _ in range(iterations):
        x = rand()
        y = rand()
        if x * x + y * y <= 1.0:
            local_hits += 1
    return local_hits  # reduction happens once, in the parent, after join


def run_with_processes(n_total: int, n_workers: int) -> tuple[float, float]:
    base = n_total // n_workers
    remainder = n_total % n_workers
    chunks = [base + (1 if i < remainder else 0) for i in range(n_workers)]

    start = time.perf_counter()
    if n_workers == 1:
        partials = [worker_chunk(chunks[0], seed=0)]
    else:
        with mp.Pool(processes=n_workers) as pool:
            partials = pool.starmap(
                worker_chunk, [(c, seed) for seed, c in enumerate(chunks)]
            )
    elapsed = time.perf_counter() - start

    total_hits = sum(partials)  # <-- the single reduction step
    pi_estimate = 4 * total_hits / n_total
    return pi_estimate, elapsed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=100_000_000)
    parser.add_argument(
        "--threads", type=int, nargs="+", default=[1, 2, 4, 8, 16, 32]
    )
    args = parser.parse_args()

    print(f"Part 3: N = {args.n:,} points, reduction pattern, multiprocessing")
    print(f"Detected CPU cores: {mp.cpu_count()}\n")

    results = {}
    for T in args.threads:
        pi_est, elapsed_ms = run_with_processes(args.n, T)
        elapsed_ms_val = elapsed_ms * 1000
        results[T] = elapsed_ms_val
        print(f"T={T:>2}  runtime={elapsed_ms_val:>9.1f} ms   pi~={pi_est:.6f}")

    baseline = results[args.threads[0]]
    print("\n| Threads (T) | Runtime (ms) | Speedup (T1/TN) | Efficiency (Speedup/T) |")
    print("|---|---|---|---|")
    for T in args.threads:
        speedup = baseline / results[T]
        efficiency = speedup / T * 100
        print(f"| {T} | {results[T]:.1f} | {speedup:.2f}x | {efficiency:.0f}% |")
