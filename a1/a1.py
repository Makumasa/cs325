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
    """
    Naive divide and conquer algorithm for pre-sorted x
    :param data: input data sorted by x
    :return:
    """
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
        # compute separation line L - O(n)
        m = n / 2
        L = data[m][0]
        left = data[:m]
        right = data[m:]

        # recurse - 2T(n/2)
        distance1, points1 = naive(left)
        distance2, points2 = naive(right)

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
        m_y = []
        for x, y in data:
            distance = abs(x - L)
            if distance < 2 * smallest_distance:
                m_y.append((x, y))

        # sort by y - O(n log n)
        mergeSort(m_y, 1)

        # get cross pairs - O(n)
        smallest_distance, points = closest_cross_pair(m_y, (smallest_distance, points))

    return smallest_distance, points


def enhanced(data_x, data_y):
    """
    Enhanced divide and conquer algorithm for pre-sorted x and y
    :param data_x: input data sorted by x
    :param data_y: input data sorted by y
    :return:
    """
    n = len(data_x)
    smallest_distance = None
    points = []

    if n == 2:
        # if there are only two points return them - O(c)
        x1, y1 = data_x[0]
        x2, y2 = data_x[1]
        smallest_distance = hypot(x2 - x1, y2 - y1)
        points = [(data_x[0], data_x[1])]
    elif n == 3:
        # if there are only three points return best of three - O(c)
        x1, y1 = data_x[0]
        x2, y2 = data_x[1]
        x3, y3 = data_x[2]
        result1 = hypot(x2 - x1, y2 - y1)
        result2 = hypot(x2 - x3, y2 - y3)
        result3 = hypot(x1 - x3, y1 - y3)
        smallest_distance = min(result1, result2, result3)
        if smallest_distance == result1:
            points = [(data_x[0], data_x[1])]
        elif smallest_distance == result2:
            points = [(data_x[1], data_x[2])]
        else:
            points = [(data_x[0], data_x[2])]
    else:
        # compute seperation line L - O(n log n)
        m = n / 2
        L = data_x[m][0]
        left_x = data_x[:m]
        right_x = data_x[m:]

        # scan and build left_y and right_y based on x coordinate - O(n)
        left_y = []
        right_y = []
        for x, y in data_y:
            if x < L:
                left_y.append((x, y))
            else:
                right_y.append((x, y))

        # recurse - 2T(n/2)
        distance1, points1 = enhanced(left_x, left_y)
        distance2, points2 = enhanced(right_x, right_y)

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

        # identify all points in data_y within delta from L - O(n)
        m_y = []
        for x, y in data_y:
            distance = abs(x - L)
            if distance < 2*smallest_distance:
                m_y.append((x, y))

        # get cross pairs - O(n)
        smallest_distance, points = closest_cross_pair(m_y, (smallest_distance, points))

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

if __name__ == "__main__":
    data_x = read_input()
    data_y = data_x

    mergeSort(data_x, 0)
    mergeSort(data_y, 0)

    print "----- Brute Force -----"
    output = brute_force(data_x)
    points = sorted(output[1], key=lambda tuple: tuple[0])
    print output[0]
    for pair1, pair2 in points:
        print pair1, pair2

    print "----- Naive -----"
    output = naive(data_x)
    points = sorted(output[1], key=lambda tuple: tuple[0])
    print output[0]
    for pair1, pair2 in points:
        print pair1, pair2

    print "----- Enhanced -----"
    output = enhanced(data_x, data_y)
    points = sorted(output[1], key=lambda tuple: tuple[0])
    print output[0]
    for pair1, pair2 in points:
        print pair1, pair2