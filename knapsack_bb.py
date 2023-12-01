import numpy as np
from scipy.optimize import linprog
from itertools import combinations
import time


# same as last week (only added the feasibility check)
def knapsack_LP(p, w, C, bounds):
    c = -p
    A = [w]
    b = [C]
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds)

    if result.success:
        value = -result.fun
        solution = result.x
    else:
        value = -np.inf  # infeasible solution :(
        solution = None

    return value, solution

# same as last week
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


def branch_and_bound_knapsack(n, p, w, C):

    best_val = 0
    best_sol = None
    subproblems = [([(0, 1)] * n)]  # list each items bounds (0,1)

    # while subproblmes are left
    while subproblems:
        # this is essentially a DFS approach, so no fancy heuristics for picking the next subproblem
        bounds = subproblems.pop()  # get bounds

        val, sol = knapsack_LP(p, w, C, bounds)  # solve lp relaxation

        if val <= best_val or val == -np.inf:  # prune if infeasible or worse than current best
            continue

        if all(x in [0, 1] for x in sol):  # check integrality
            if val > best_val:
                best_val = val
                best_sol = sol
        else:
            # branch on fractional var
            for i, x in enumerate(sol):
                if not x.is_integer():
                    # exclude
                    exclude_bounds = bounds.copy()
                    exclude_bounds[i] = (0, 0)
                    subproblems.append(exclude_bounds)

                    # include
                    include_bounds = bounds.copy()
                    include_bounds[i] = (1, 1)
                    subproblems.append(include_bounds)
                    break  # we know there is max 1 fractional var so we can break

    # get item indices
    indices = [i for i, x in enumerate(best_sol) if x == 1]
    return best_val, indices


if __name__ == '__main__':
    n = 20
    C = 879
    p = np.array([91, 72, 90, 46, 55, 8, 35, 75, 61, 15, 77, 40, 63, 75, 29, 75, 17, 78, 40, 44])
    w = np.array([84, 83, 43, 4, 44, 6, 82, 92, 25, 83, 56, 18, 58, 14, 48, 70, 96, 32, 68, 92])

    start = time.time()
    val, sol = branch_and_bound_knapsack(n, p, w, C)
    end = time.time()
    print("n = 20")
    print("Branch and bound Time: " + str(round(end - start, 4)) + " seconds")
    print("Optimal value: " + str(val))

    start = time.time()
    val, _ = knapsack_brute_force(p, w, C)
    end = time.time()
    print("Brute force Time: " + str(round(end - start, 4)) + " seconds")
    print("Optimal value: " + str(val))

    # check for instance+2 (3 takes like 30+ seconds)
    n3 = 22
    p3 = np.concatenate((p, [1, 2]))
    w3 = np.concatenate((w, [1, 2]))


    start = time.time()
    val, sol = branch_and_bound_knapsack(n3, p3, w3, C)
    end = time.time()
    print("\nn = 22")
    print("Branch and bound Time: " + str(round(end - start, 4)) + " seconds")
    print("Optimal value: " + str(val))

    start = time.time()
    val, _ = knapsack_brute_force(p3, w3, C)
    end = time.time()
    print("Brute force Time: " + str(round(end - start, 4)) + " seconds")
    print("Optimal value: " + str(val))


