
with open("Corvallis.csv", 'r') as f:
    lines = f.readlines(22305)

data_set = []
for line in lines[1:]:
    data_list = line.replace('\r\n', '').split(';')
    data_dict = {}
    data_dict["STATION"] = data_list[0]
    data_dict["DATE"] = data_list[1]
    data_dict["TMAX"] = data_list[2]
    data_dict["TMIN"] = data_list[3]
    data_dict["year"] = data_list[4]
    data_dict["month"] = data_list[5]
    data_dict["day"] = data_list[6]
    data_dict["average"] = data_list[7]
    data_dict["time"] = data_list[8]

print data_list