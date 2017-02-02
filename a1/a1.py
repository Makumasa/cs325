#!/usr/bin/env python
from math import hypot

def read_input(filepath="example.input"):
    data_list = []

    with open(filepath, 'r') as f:
        input_data = f.readlines()

    input_data = [x.strip() for x in input_data]
    for line in input_data:
        x, y = line.split(' ')
        data_list.append((int(x), int(y)))

    return data_list


def mergeSort(alist, member=0):
    """
    Implementation found at:
    http://interactivepython.org/courselib/static/pythonds/SortSearch/TheMergeSort.html

    Adapted to take list of tuples and sort given member.
    """
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf, member)
        mergeSort(righthalf, member)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][member] < righthalf[j][member]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1


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
    if n == 2:
        # if there are only two points return them - O(c)
        x1, y1 = data[0]
        x2, y2 = data[1]
        smallest_distance = hypot(x2 - x1, y2 - y1)
        points = [(data[0], data[1])]
    elif n == 3:
        # if there are only three points return best of three - O(c)
        x1, y1 = data[0]
        x2, y2 = data[1]
        x3, y3 = data[2]
        result1 = hypot(x2 - x1, y2 - y1)
        result2 = hypot(x2 - x3, y2 - y3)
        result3 = hypot(x1 - x3, y1 - y3)
        smallest_distance = min(result1, result2, result3)
        if smallest_distance == result1:
            points = [(data[0], data[1])]
        elif smallest_distance == result2:
            points = [(data[1], data[2])]
        else:
            points = [(data[0], data[2])]
    else:
        # split data in half - O(n)
        m = n/2
        left = data[:m]
        right = data[m:]

        # recurse - O(log n)
        distance1, points1 = naive(left)
        distance2, points2 = naive(right)

        # combine - O(c)
        if distance1 == distance2:
            smallest_distance = distance1
            points = points1 + points2
        elif distance1 > distance2:
            smallest_distance = distance2
            points = points2
        elif distance1 < distance2:
            smallest_distance = distance1
            points = points1
	
        # identify all points within delta from L - O(n)
        M_y = []
        for x, y in data:
            distance = abs(x - L)
            if distance < 2*smallest_distance:
                M_y.append((x, y))

        # sort by y - O(n log n)
        mergeSort(M_y, 1)

 
        smallest_distance, points = closest_cross_pair(M_y, (smallest_distance, points))

        # check cross pairs - O((n/2)^2)
        #for x1, y1 in left:
        #    for x2, y2 in right:
        #        result = hypot(x2 - x1, y2 - y1)
        #        if result < smallest_distance:
        #            smallest_distance = result
        #            points = [((x1, y1), (x2, y2))]
        #        elif result == smallest_distance:
        #            points += [((x1, y1), (x2, y2))]

    return smallest_distance, points


def enhanced(data_X, data_Y):

    #Uli: Since we keep dividing both datasets at their midpoint they should both contain the same number of elements
    n = len(data_X)
    smallest_distance = None
    points = []

    if n == 2:
        # if there are only two points return them - O(c)
        x1, y1 = data[0]
        x2, y2 = data[1]
        smallest_distance = hypot(x2 - x1, y2 - y1)
        points = [(data[0], data[1])]
    elif n:
        # if there are only three points return best of three - O(c)
        x1, y1 = data[0]
        x2, y2 = data[1]
        x3, y3 = data[2]
        result1 = hypot(x2 - x1, y2 - y1)
        result2 = hypot(x2 - x3, y2 - y3)
        result3 = hypot(x1 - x3, y1 - y3)
        smallest_distance = min(result1, result2, result3)
        if smallest_distance == result1:
            points = [(data[0], data[1])]
        elif smallest_distance == result2:
            points = [(data[1], data[2])]
        else:
            points = [(data[0], data[2])]
    else:
        # compute seperation line L - O(n log n)
        
	#From the description, we may assume data_X to be sorted by X and data_Y to be sorted by Y
	#mergeSort(data, 0)

        m = n / 2
        L_X = data_X[m][0]
	L_Y = data_Y[m][0]

        # recurse - 2T(n/2)
	distance1, points1 = enhanced(data_X[:m], data_Y[:m])
	distance2, points2 = enhanced(data_X[m:], data_Y[:m])

        # get starting delta - O(c)
        if distance1 == distance2:
            smallest_distance = distance1
            points = points1 + points2
        elif distance1 > distance2:
            smallest_distance = distance2
            points = points2
        elif distance1 < distance2:
            smallest_distance = distance1
            points = points1

        # identify all points within delta from L - O(n)
	#Uli: This needs to somehow apply to data_Y? Her email was really confusing.
        M_y = []
        for x, y in data:
            distance = abs(x - L)
            if distance < 2*smallest_distance:
                M_y.append((x, y))

        # sort by y - O(n log n)
        mergeSort(M_y, 1)

        # get cross pairs - O(n)
        smallest_distance, points = closest_cross_pair(M_y, (smallest_distance, points))

    return smallest_distance, points


def closest_cross_pair(data, start):
    d_m = start[0]
    points = start[1]
    m = len(data)

    for i in range(0, m-1):
        j = i + 1
        while data[j][1] - data[i][1] <= d_m:
            x1, y1 = data[j]
            x2, y2 = data[i]
            d = hypot(x2 - x1, y2 - y1)
            if d < d_m:
                d_m = d
                points = [(data[i], data[j])]
            elif d == d_m:
                if (data[i], data[j]) not in points:
                    points += [(data[i], data[j])]

            if j == m-1:
                break
            else:
                j += 1

    return d_m, points

# TODO: sort output
if __name__ == "__main__":
    data = read_input()

    print "----- Brute Force -----"
    output = brute_force(data)
    points = sorted(output[1], key=lambda tuple: tuple[0])
    print output[0]
    for pair1, pair2 in points:
        print pair1, pair2

    print "----- Naive -----"
    output = naive(data)
    points = sorted(output[1], key=lambda tuple: tuple[0])
    print output[0]
    for pair1, pair2 in points:
        print pair1, pair2

    print "----- Enhanced -----"
    output = enhanced(data)
    points = sorted(output[1], key=lambda tuple: tuple[0])
    print output[0]
    for pair1, pair2 in points:
        print pair1, pair2
