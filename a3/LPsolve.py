# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from pulp import *
from math import *

with open("Corvallis.csv", 'r') as f:
    lines = f.readlines()

data_set = []
for line in lines[1:]:
    data_list = line.replace('\r\n', '').split(';')
    data_dict = {}
    data_dict["station"] = data_list[0]
    data_dict["date"] = data_list[1]
    data_dict["tmin"] = data_list[2]
    data_dict["tmax"] = data_list[3]
    data_dict["year"] = data_list[4]
    data_dict["month"] = data_list[5]
    data_dict["day"] = data_list[6]
    data_dict["average"] = data_list[7]
    data_dict["time"] = data_list[8]

    data_set.append(data_dict)

print len(data_set)

x0 = LpVariable("x0") #0 <= x0
x1 = LpVariable("x1") #0 <= x1
x2 = LpVariable("x2") #0 <= x2
x3 = LpVariable("x3") #0 <= x3
x4 = LpVariable("x4") #0 <= x4
x5 = LpVariable("x5") #0 <= x5

#What we'll be optimizing for
U = LpVariable("U")

prob = LpProblem("MMAD", LpMinimize)

graph_x = []
graph_y = []
for data in data_set:

   d = int(data["time"])
   avg_temp = float(data["average"])

   graph_x.append(d)
   graph_y.append(avg_temp)

   prob += (x0 + x1 * d + 							#linear trend
            x2 * cos(2*pi*d/365.25) + x3 * sin(2*pi*d/365.25) + 		#seasonal pattern
            x4 * cos(2*pi*d/(365.25*10.7)) + x5 * sin(2*pi*d/(365.25*10.7))	#solar cycle
            - avg_temp) <= U
   
   prob += -(x0 + x1 * d + 							#linear trend
            x2 * cos(2*pi*d/365.25) + x3 * sin(2*pi*d/365.25) + 		#seasonal pattern
            x4 * cos(2*pi*d/(365.25*10.7)) + x5 * sin(2*pi*d/(365.25*10.7))	#solar cycle
            - avg_temp) <= U

#Function to minimize
prob += U

status = prob.solve()
LpStatus[status]

#Print the result for a and b:
print LpStatus[status]
print "Obejective Value:", value(U)
print "x0 =", value(x0)
print "x1 =", value(x1)
print "x2 =", value(x2)
print "x3 =", value(x3)
print "x4 =", value(x4)
print "x5 =", value(x5)


plt.scatter(graph_x, graph_y, s=1)
best_fit_y = []
best_fit_linear = []
for d in graph_x:
    val = abs(value(x0) + value(x1) * d +  # linear trend
             value(x2) * cos(2 * pi * d / 365.25) + value(x3) * sin(2 * pi * d / 365.25) +  # seasonal pattern
             value(x4) * cos(2 * pi * d / (365.25 * 10.7)) + value(x5) * sin(2 * pi * d / (365.25 * 10.7)))  # solar cycle

    best_fit_linear.append(value(x0) + value(x1) * d)
    best_fit_y.append(val)

plt.scatter(graph_x, best_fit_linear, s=1, color="red")
plt.scatter(graph_x, best_fit_y, s=1, color="green")
plt.xlabel('Days Since May 1, 1952')
ylabel_string = ''
ylabel_string += 'Temperature ('
ylabel_string += u'\u00b0'
ylabel_string += "C)"
plt.ylabel(ylabel_string)
plt.title('Corvallis Temperature vs. Days Since May 1, 1952')
plt.legend(markerscale=10)
plt.show()