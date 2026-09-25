import threading
import time
import math
import os


# Искусственная нагрузка для одного потока
def worker():
    result = 0.0

    for i in range(10_000_000):
        result += math.sqrt(i + 1)

    return result


def run_threads(P):
    threads = []

    start = time.perf_counter()

    # Создаем P потоков
    for _ in range(P):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

    end = time.perf_counter()

    return end - start


def main():

    P_values = [1, 2, 4, 8, 16, 32, 64]

    print("=" * 65)
    print("TASK 1.3: CPU CORE SATURATION ANALYSIS")
    print("=" * 65)

    print("Logical CPU cores:", os.cpu_count())
    print()
    print("Workload per thread: 10,000,000 square roots")
    print()

    print(f"{'P':>5} {'Execution Time (s)':>25}")
    print("-" * 35)

    results = []

    for P in P_values:

        print(f"Running P = {P} ...")

        execution_time = run_threads(P)

        results.append((P, execution_time))

        print(f"{P:>5} {execution_time:>25.4f}")

    # Сохраняем результаты
    with open("task1_3_results.csv", "w") as file:

        file.write("P,execution_time_seconds\n")

        for P, execution_time in results:
            file.write(f"{P},{execution_time:.6f}\n")

    print()
    print("Results saved to: task1_3_results.csv")


if __name__ == "__main__":
    main()