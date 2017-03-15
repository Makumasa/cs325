from pulp import *
from math import *

with open("Corvallis.csv", 'r') as f:
    lines = f.readlines(22305)

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

x0 = LpVariable("x0") #0 <= x0
x1 = LpVariable("x1") #0 <= x1
x2 = LpVariable("x2") #0 <= x2
x3 = LpVariable("x3") #0 <= x3
x4 = LpVariable("x4") #0 <= x4
x5 = LpVariable("x5") #0 <= x5

#What we'll be optimizing for
U = LpVariable("U")

prob = LpProblem("MMAD", LpMinimize)

for data in data_set:

   d = int(data["time"])
   avg_temp = float(data["average"])

   prob +=   (x0 + x1 * d + 							#linear trend
	     x2 * cos(2*pi*d/365.25) + x3 * sin(2*pi*d/365.25) + 		#seasonal pattern
	     x4 * cos(2*pi*d/(365.25*10.7)) + x5 * sin(2*pi*d/(365.25*10.7))	#solar cycle
	     - avg_temp) <= U
   
   prob +=  -(x0 + x1 * d + 							#linear trend
	     x2 * cos(2*pi*d/365.25) + x3 * sin(2*pi*d/365.25) + 		#seasonal pattern
	     x4 * cos(2*pi*d/(365.25*10.7)) + x5 * sin(2*pi*d/(365.25*10.7))	#solar cycle
	     - avg_temp) <= U

#Function to minimize
prob += U

status = prob.solve()
LpStatus[status]

#Print the result for a and b:
print value(x0)
print value(x1)
print value(x2)
print value(x3)
print value(x4)
print value(x5)
