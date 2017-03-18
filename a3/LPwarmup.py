import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pulp import *
test_set = [(1, 3), (2, 5), (3, 7), (5, 11), (7, 14), (8, 15), (10, 19)]

# Objective Function:  max( | ax + b - y | )
prob = LpProblem("mmat", LpMinimize)
a = LpVariable("a")
b = LpVariable("b")
U = LpVariable("U")

for x, y in test_set:
    prob += (a*x + b - y) <= U
    prob += -(a*x + b - y) <= U

prob += U

# Solve the problem
status = prob.solve()
print LpStatus[status]
print "Obejective Value:", value(U)
print "a =", value(a), "b =", value(b)

# Build and plot our best fit line
plt.scatter(*zip(*test_set))
best_fit_x = []
best_fit_y = []
for x, y in test_set:
    best_fit_x.append(x)
    best_fit_y.append(value(a) * x + value(b))

plt.plot(best_fit_x, best_fit_y)
plt.xticks(np.arange(0, math.ceil(max(best_fit_x)) + 1, 1.0))
plt.yticks(np.arange(0, math.ceil(max(best_fit_y)) + 1, 1.0))
plt.axis('scaled')
plt.xlabel('x')
plt.ylabel('y')
plt.show()