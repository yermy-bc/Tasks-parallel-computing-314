#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <omp.h>
#include <cstdlib>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: benchmark.exe <threads>\n";
        return 1;
    }

    int threads = atoi(argv[1]);
    if (threads < 1) return 1;

    const int N = 1200;  // Compute-heavy matrix size
    const int RUNS = 3;

    vector<double> A(N * N), B(N * N), C(N * N);

    mt19937 rng(42);
    uniform_real_distribution<double> dist(0.0, 1.0);

    for (auto &x : A) x = dist(rng);
    for (auto &x : B) x = dist(rng);

    omp_set_num_threads(threads);

    cout << "Threads: " << threads << "\n";
    cout << "Matrix size: " << N << " x " << N << "\n";

    double total = 0.0;

    for (int run = 1; run <= RUNS; run++) {
        fill(C.begin(), C.end(), 0.0);

        auto start = chrono::high_resolution_clock::now();

        #pragma omp parallel for schedule(static)
        for (int i = 0; i < N; i++) {
            for (int k = 0; k < N; k++) {
                double aik = A[i * N + k];
                for (int j = 0; j < N; j++) {
                    C[i * N + j] += aik * B[k * N + j];
                }
            }
        }

        auto end = chrono::high_resolution_clock::now();
        double seconds = chrono::duration<double>(end - start).count();

        cout << "Run " << run << ": " << seconds << " s\n";
        total += seconds;
    }

    cout << "Average: " << total / RUNS << " s\n";
    return 0;
}
