#!/usr/bin/env python
from a1 import *
from sys import argv, exit

if __name__ == "__main__":
    argc = len(argv)
    if argc != 2:
        print "Usage: enhanceddnc.py input_file"
        exit()

    filepath = argv[1]
    data_x = read_input()
    data_y = data_x

    mergeSort(data_x, 0)
    mergeSort(data_y, 1)

    output = enhanced(data_x, data_y)
    points = sorted(output[1], key=lambda tuple: tuple[0])
    print output[0]
    for pair1, pair2 in points:
        print pair1, pair2

    with open("output.enhanceddnc.txt", 'w') as f:
        f.write(str(output[0]) + "\n\r")
        for pair1, pair2 in points:
            f.write(str(pair1) + " " + str(pair2) + "\n\r")

