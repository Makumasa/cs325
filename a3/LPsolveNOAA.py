from pulp import *
from math import *

with open("Climate/baseorcadas.csv", 'r') as f:
    lines = f.readlines()

data_set = []
for line in lines[1:]:
    data_list = line.replace('\r\n', '').split(',')
    data_dict = {}
    data_dict["station"] = data_list[0]
    data_dict["name"] = data_list[1]
    data_dict["date"] = data_list[2]
    data_dict["tavg"] = data_list[3]
    data_dict["tmax"] = data_list[4]
    data_dict["tmin"] = data_list[5]
    
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
   
   d = int(data["date"])
   avg_temp = float(data["tavg"])
   max_temp = float(data["tmax"])
   min_temp = float(data["tmin"])

   if avg_temp == -9999:
   	if max_temp != -9999 and min_temp != -9999:
		avg_temp = (max_temp-min_temp)/2
	else:
		print "Skipped an entry"

   if avg_temp != -9999:
   	prob +=  (x0 + x1 * d + 							#linear trend
		 x2 * cos(2*pi*d/365.25) + x3 * sin(2*pi*d/365.25) + 			#seasonal pattern
	    	 x4 * cos(2*pi*d/(365.25*10.7)) + x5 * sin(2*pi*d/(365.25*10.7))	#solar cycle
	    	 - avg_temp) <= U

	prob +=  -(x0 + x1 * d + 							#linear trend
	     	 x2 * cos(2*pi*d/365.25) + x3 * sin(2*pi*d/365.25) + 			#seasonal pattern
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
