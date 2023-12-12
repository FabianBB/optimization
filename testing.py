from scipy.optimize import linprog
import numpy as np

def knapsack_LP(n, p, w, C, bounds=None):
    b = np.array([C])
    A = np.array([w])
    c = np.array([-a for a in p])
    if bounds is None:
        bounds = np.array([(0, 1) for i in range(n)])
    ret = linprog(c, A_ub=A, b_ub=b, bounds=bounds)
    if ret.status == 0:
        return (-ret.fun, ret.x)
    else:
        return None


def knapsack(n, p, w, C):
    init = np.array([(0, 1) for i in range(n)])
    active = [init]
    best = -1
    arg_best = None
    while len(active) > 0:
        bounds = active.pop()
        lp = knapsack_LP(n, p, w, C, bounds)
        if lp is None:
            continue
        fun, x = lp
        if fun < best:
            continue
        i = -1
        for j in range(n):
            if x[j] < 0.999 and x[j] > 0.001:
                i = j
                break
        if i == -1: #is integral
            if fun > best:
                best = fun
                arg_best = x
        else: #not integral
            zero = np.copy(bounds)
            zero[i] = (0, 0)
            bounds[i] = (1, 1)
            active.append(zero)
            active.append(bounds)
    return (best, arg_best)

def configuration_LP(n, s, C):
    no_bins = 0
    bins = []

    # go until all are packed
    remaining_items = set(range(n))  # unpacked stuff

    while remaining_items:
        # solve knap for remaining
        p = [1 if i in remaining_items else 0 for i in range(n)]  # profit is 1 ONLY for remaining items
        w = [s[i] if i in remaining_items else 0 for i in range(n)]  # weight is item size

        _, knapsack_solution = knapsack_LP(n, p, w, C)
        if knapsack_solution is None:
            break

        # new bin based on lp solutoin
        new_bin = [0] * n
        for i in range(n):
            if knapsack_solution[i] > 0.5 and i in remaining_items:  # ONLY UNPACKED
                new_bin[i] = 1
                remaining_items.remove(i)

        # add to bins
        bins.append(new_bin)
        no_bins += 1

    return (no_bins, bins)


if __name__ == '__main__':


    n1 = 30
    S1 = 150
    s1 = [34, 51, 23, 51, 49, 51, 60, 26, 44, 47, 76, 72, 62, 37, 58, 53, 72, 22, 88,
    75, 85, 43, 54, 30, 77, 36, 33, 56, 67, 43]

    n2 = 120
    S2 = 150
    s2 = [72, 62, 48, 59, 26, 81, 82, 77, 27, 82, 86, 87, 50, 93, 93, 42, 84, 47, 44,
    64, 87, 46, 37, 27, 45, 20, 23, 66, 60, 43, 58, 48, 32, 85, 87, 76, 72, 100, 66,
    63, 53, 44, 60, 96, 56, 62, 23, 95, 61, 70, 86, 78, 43, 36, 93, 79, 69, 98, 65, 45,
    90, 31, 97, 66, 75, 74, 80, 98, 68, 32, 88, 31, 78, 41, 57, 45, 36, 82, 26, 78, 44,
    92, 78, 53, 38, 55, 56, 26, 98, 32, 67, 90, 22, 24, 41, 31, 97, 35, 39, 42, 72, 56,
    85, 34, 75, 51, 22, 96, 99, 35, 37, 94, 59, 45, 99, 47, 41, 53, 67, 74]

    sol1 = configuration_LP(n1, s1, S1)
    sol2 = configuration_LP(n2, s2, S2)
    print("Problem 1")
    print(sol1)
    readable_output = [[i for i, is_in_bin in enumerate(bin_config) if is_in_bin == 1] for bin_config in sol1[1]]
    print("readable output")
    print(readable_output)

    print("\nProblem 2")
    print(sol2)
    readable_output = [[i for i, is_in_bin in enumerate(bin_config) if is_in_bin == 1] for bin_config in sol2[1]]
    print("readable output")
    print(readable_output)
