from pulp import *
points = [(1,3), (2,5), (3,7), (5,11), (7,14), (8,15), (10,19)]

a = LpVariable("a") #0 <= x
b = LpVariable("b") #0 <= b

#What we'll be optimizing for
U = LpVariable("U")

prob = LpProblem("MMAD", LpMinimize)

for x,y in points:
   prob +=  (a*x + b - y) <= U
   prob += -(a*x + b - y) <= U

#Function to minimize
prob += U

status = prob.solve()
LpStatus[status]

#Print the result for a and b:
print value(a)
print value(b)
