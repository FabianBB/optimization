from scipy.optimize import linprog
import numpy as np
import random
import itertools


def knapsack_LP(n, p, w, C):
    # max profits i.e. min neg profits
    c = -p  # linprog minimizes by default so * -1

    # The weights are the constraints that must be less than or equal to the capacity
    A = [w]  # The weights are the coefficients for the inequality constraints
    b = [C]  # The capacity is the upper bound for the inequality constraint

    # greater than 0 and less than 1 since relaxation
    x_bounds = [(0, 1) for _ in range(n)]

    # result
    result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds)

    # do *-1 again since we did negative profits
    value = -result.fun
    solution = result.x

    # make super beautiful output
    # item_selection = {f'Item {i+1}': x for i, x in enumerate(solution)} # to show which item
    item_selection = [x for i, x in enumerate(solution)]

    return value, item_selection


n = 20
# capacity
C = 879
# profits
p = np.array([91, 72, 90, 46, 55, 8, 35, 75, 61, 15, 77, 40, 63, 75, 29, 75, 17, 78, 40, 44])
# weights
w = np.array([84, 83, 43, 4, 44, 6, 82, 92, 25, 83, 56, 18, 58, 14, 48, 70, 96, 32, 68, 92])

val, sol = knapsack_LP(n, p, w, C)

print(f"Optimal value: {val}")
print(f"Optimal solution: {sol}")
