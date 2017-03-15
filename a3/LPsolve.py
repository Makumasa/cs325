from pulp import *
from math import *

x0 = LpVariable("x0") #0 <= x0
x1 = LpVariable("x1") #0 <= x1
x2 = LpVariable("x2") #0 <= x2
x3 = LpVariable("x3") #0 <= x3
x4 = LpVariable("x4") #0 <= x4
x5 = LpVariable("x5") #0 <= x5

#What we'll be optimizing for
U = LpVariable("U")

prob = LpProblem("MMAD", LpMinimize)

for x,y in points:

   prob +=   (x0 + x1 * d + 							#linear trend
	     x2 * cos(2*pi*d/365.25) + x3 * sin(2*pi*d/365.25) + 		#seasonal pattern
	     x4 * cos(2*pi*d/(365.25*10.7)) + x5 * sin(2*pi*d/(365.25*10.7))	#solar cycle
	     ) <= U
   
   prob +=  -(x0 + x1 * d + 							#linear trend
	     x2 * cos(2*pi*d/365.25) + x3 * sin(2*pi*d/365.25) + 		#seasonal pattern
	     x4 * cos(2*pi*d/(365.25*10.7)) + x5 * sin(2*pi*d/(365.25*10.7))	#solar cycle
	     ) <= U

#Function to minimize
prob += U

status = prob.solve()
LpStatus[status]

#Print the result for a and b:
print value(a)
print value(b)
