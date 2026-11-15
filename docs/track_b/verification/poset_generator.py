"""
poset_generator.py
Generates all 5,231 naturally ordered posets of size N <= 6.
"""

import numpy as np

def generate_naturally_ordered_posets(max_N=6):
    """
    Yields (N, C) for all naturally ordered transitive DAGs (posets) up to max_N.
    C is strictly lower-triangular with zero diagonal.
    Total counts:
      N=1: 1
      N=2: 2
      N=3: 7
      N=4: 40
      N=5: 357
      N=6: 4824
      Total (N <= 6): 5,231 posets.
    """
    for N in range(1, max_N + 1):
        num_edges = N * (N - 1) // 2
        indices = [(i, j) for i in range(N) for j in range(i)]
        for mask in range(1 << num_edges):
            C = np.zeros((N, N), dtype=float)
            for idx, (r, c) in enumerate(indices):
                if (mask >> idx) & 1:
                    C[r, c] = 1.0
            C2 = C @ C
            if np.all((C2 == 0) | (C == 1)):
                yield N, C

if __name__ == "__main__":
    counts = {n: 0 for n in range(1, 7)}
    for N, C in generate_naturally_ordered_posets(6):
        counts[N] += 1
    print("Poset counts by N:", counts)
    print("Total posets:", sum(counts.values()))
    assert sum(counts.values()) == 5231
