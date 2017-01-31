from math import hypot
import timeit

def read_input(filepath="example.input"):
    data_list = []

    with open(filepath, 'r') as f:
        input_data = f.readlines()

    input_data = [x.strip() for x in input_data]
    for line in input_data:
        x, y = line.split(' ')
        data_list.append((int(x), int(y)))

    return data_list

def brute_force(data):
    smallest_distance = None
    points = []
    for x1, y1 in data:
        for x2, y2 in data:
            result = hypot(x2-x1, y2-y1)
            if result != 0:
                if result < smallest_distance or smallest_distance is None:
                    smallest_distance = result
                    points = [((x1, y1), (x2, y2))]
                elif result == smallest_distance:
                    if ((x2, y2), (x1, y1)) not in points:
                        points.append(((x1, y1), (x2, y2)))

    return smallest_distance, points

def naive(data):
    n = len(data)
    smallest_distance = None
    points = []
    if n <= 3:
        for x1, y1 in data:
            for x2, y2 in data:
                result = hypot(x2 - x1, y2 - y1)
                if result != 0:
                    if result < smallest_distance or smallest_distance is None:
                        smallest_distance = result
                        points = [((x1, y1), (x2, y2))]
                    elif result == smallest_distance:
                        if ((x2, y2), (x1, y1)) not in points:
                            points.append(((x1, y1), (x2, y2)))
    else:
        m = n/2
        data1 = data[:m]
        data2 = data[m:]
        distance1, points1 = naive(data1)
        distance2, points2 = naive(data2)
        if distance1 == distance2:
            smallest_distance = distance1
            points = points1 + points2
        elif distance1 > distance2:
            smallest_distance = distance2
            points = points2
        elif distance1 < distance2:
            smallest_distance = distance1
            points = points1

    return smallest_distance, points

if __name__ == "__main__":
    data = read_input()
    start = time.time()
    output = naive(data)
    stop = time.time()
    print "Completed in:", stop-start

    print output[0]
    for pair1, pair2 in output[1]:
        print pair1, pair2