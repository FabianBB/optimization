%pip install scipy
from scipy.optimize import linprog
import numpy as np
import random
import itertools

def knapsack_LP(n, p, w, C):
    # familiarize yourself with numpy arrays (for matrices and vectors):
    # https://numpy.org/doc/stable/reference/generated/numpy.array.html
    # and with linprog (scipy): 
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    value = 0
    solution = np.zeros(n)
    return (value, solution)

n = 20
C = 879
p = np.array([91, 72, 90, 46, 55, 8, 35, 75, 61, 15, 77, 40, 63, 75, 29, 75, 17, 78, 40, 44])
w = np.array([84, 83, 43, 4, 44, 6, 82, 92, 25, 83, 56, 18, 58, 14, 48, 70, 96, 32, 68, 92])

print(knapsack_LP(n, p, w, C))