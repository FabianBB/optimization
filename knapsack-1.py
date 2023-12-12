from scipy.optimize import linprog
import numpy as np
import random
import itertools

def knapsack_LP(n, p, w, C, bounds=None):
  b = np.array([C])
  A = np.array([w])
  c = np.array([-a for a in p])
  if bounds is None:
    bounds = np.array([(0, 1) for i in range(n)])
  ret = linprog(c, A_ub = A, b_ub = b, bounds=bounds)
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
  # Add your code here
  return (no_bins, bins)



# ... (Your existing knapsack_LP and other functions here) ...

def configuration_LP_with_column_generation(n, s, C):
    # Step 1: Initialize RMP
    # Start with each item in its bin (basic feasible solution)
    initial_configs = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    bin_usage = [1 for _ in range(n)]  # each bin used once initially
    bins = list(zip(initial_configs, bin_usage))

    while True:
        # Step 2: Solve the Knapsack Subproblem
        # Construct the dual prices for each item
        dual_prices = [0] * n  # initialize with zero
        for config, usage in bins:
            for i, included in enumerate(config):
                if included:
                    dual_prices[i] += usage

        # Find the most negative reduced cost column using knapsack
        knapsack_result = knapsack_LP(n, dual_prices, s, C)
        if knapsack_result is None:
            break  # Termination condition

        reduced_cost, new_config = knapsack_result
        if reduced_cost >= -1e-5:  # A tolerance for numerical stability
            break  # Termination condition

        # Step 3: Update the RMP
        bins.append((new_config, 1))  # Add the new configuration

    # Step 4: Termination Check is within the loop

    # Step 5: Output the solution
    no_bins = sum(bin_usage for _, bin_usage in bins)
    return no_bins, bins



def knapsack_brute_force(n, p, w, C):
  best = -1
  arg_best = None
  for x in itertools.product(range(2), repeat=n):
    vx = np.array(x)
    if np.dot(vx, w) <= C and np.dot(vx, p) > best:
      best = np.dot(vx, p)
      arg_best = vx
  return (best, arg_best)

#n = 20
#C = 879
#p = np.array([91, 72, 90, 46, 55, 8, 35, 75, 61, 15, 77, 40, 63, 75, 29, 75, 17, 78, 40, 44])
#w = np.array([84, 83, 43, 4, 44, 6, 82, 92, 25, 83, 56, 18, 58, 14, 48, 70, 96, 32, 68, 92])

#print(knapsack(n, p, w, C))

n1 = 30
C1 = 150
s1 = [34, 51, 23, 51, 49, 51, 60, 26, 44, 47, 76, 72, 62, 37, 58, 53, 72, 22, 88, 75, 85, 43, 54, 30, 77, 36, 33, 56, 67, 43]

n2 = 120
C2 = 150
s2 = [72, 62, 48, 59, 26, 81, 82, 77, 27, 82, 86, 87, 50, 93, 93, 42, 84, 47, 44, 64, 87, 46, 37, 27, 45, 20, 23, 66, 60, 43, 58, 48, 32, 85, 87, 76, 72, 100, 66, 63, 53, 44, 60, 96, 56, 62, 23, 95, 61, 70, 86, 78, 43, 36, 93, 79, 69, 98, 65, 45, 90, 31, 97, 66, 75, 74, 80, 98, 68, 32, 88, 31, 78, 41, 57, 45, 36, 82, 26, 78, 44, 92, 78, 53, 38, 55, 56, 26, 98, 32, 67, 90, 22, 24, 41, 31, 97, 35, 39, 42, 72, 56, 85, 34, 75, 51, 22, 96, 99, 35, 37, 94, 59, 45, 99, 47, 41, 53, 67, 74]

print(configuration_LP_with_column_generation(n1, s1, C1))
print(configuration_LP_with_column_generation(n2, s2, C2))
