from itertools import combinations
import time
import random


def knapsack_brute_force(values, weights, capacity):
    n = len(values)
    best_val = 0
    best_combi = ()

    # iter through all combis
    for r in range(n + 1):
        for c in combinations(range(n), r):
            current_w = sum(weights[i] for i in c)
            current_v = sum(values[i] for i in c)
            if current_w <= capacity and current_v > best_val:
                best_val = current_v
                best_combi = c

    return best_val, best_combi


# 20 items
random.seed(69)  # for reproducibility
values_20 = [random.randint(1, 100) for _ in range(20)]
weights_20 = [random.randint(1, 100) for _ in range(20)]
capacity_20 = 100

# solve 20
start_time = time.time()
best_v_20, best_combi_20 = knapsack_brute_force(values_20, weights_20, capacity_20)
time_20 = time.time() - start_time

# +3 items
values_23 = values_20 + [random.randint(1, 100) for _ in range(3)]
weights_23 = weights_20 + [random.randint(1, 100) for _ in range(3)]

# 23 items
start_time = time.time()
best_v_23, best_combi_23 = knapsack_brute_force(values_23, weights_23, capacity_20)
time_taken_23 = time.time() - start_time


print("Time for 20 items: ", time_20)
print("Time for 23 items: ", time_taken_23)
