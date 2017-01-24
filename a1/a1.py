from math import hypot
import time

def read_input(filepath="example.input"):
    data_list = []

    with open(filepath, 'r') as f:
        input_data = f.readlines()

    input_data = [x.strip() for x in input_data]
    for line in input_data:
        x, y = line.split(' ')
        data_list.append((int(x), int(y)))

    return data_list

def n_squared(data):
    smallest_distance = None
    points = []
    for x1, y1 in data:
        for x2, y2 in data:
            result = hypot(x2-x1, y2-y1)
            if result != 0:
                if smallest_distance is None:
                    smallest_distance = result
                    points = [((x1, y1), (x2, y2))]
                else:
                    if result < smallest_distance:
                        smallest_distance = result
                        points = [((x1, y1), (x2, y2))]
                    elif result == smallest_distance:
                        if ((x2, y2), (x1, y1)) not in points:
                            points.append(((x1, y1), (x2, y2)))

    return smallest_distance, points

if __name__ == "__main__":
    data = read_input()
    start = time.time()
    output = n_squared(data)
    stop = time.time()
    print "Completed in:", stop-start

    print output[0]
    for pair1, pair2 in output[1]:
        print pair1, pair2