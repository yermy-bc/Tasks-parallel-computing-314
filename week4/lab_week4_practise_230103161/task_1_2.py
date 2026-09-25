import threading
import time
import os
import csv


def worker():
    pass


def measure_time(P, repetitions=10):
    times = []

    for _ in range(repetitions):
        threads = []

        start = time.perf_counter()

        # Создание P потоков
        for _ in range(P):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()

        # Join всех потоков
        for thread in threads:
            thread.join()

        end = time.perf_counter()

        times.append(end - start)

    average_time = sum(times) / len(times)
    minimum_time = min(times)

    return average_time, minimum_time


def main():

    P_values = [1, 2, 4, 8, 16, 32, 64]

    print("=" * 60)
    print("TASK 1.2: THREAD OVERSUBSCRIPTION SWEEP")
    print("=" * 60)

    print("CPU logical processors:", os.cpu_count())
    print()

    print(f"{'P':>5} {'Average Time (s)':>20} {'Minimum Time (s)':>20}")
    print("-" * 50)

    results = []

    for P in P_values:

        average_time, minimum_time = measure_time(P)

        results.append((P, average_time, minimum_time))

        print(
            f"{P:>5} "
            f"{average_time:>20.8f} "
            f"{minimum_time:>20.8f}"
        )

    # Сохраняем результаты
    with open("task1_2_results.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "P",
            "average_time_seconds",
            "minimum_time_seconds"
        ])

        for P, average_time, minimum_time in results:
            writer.writerow([
                P,
                average_time,
                minimum_time
            ])

    print()
    print("Results saved to: task1_2_results.csv")


if __name__ == "__main__":
    main()