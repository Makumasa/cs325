#!/usr/bin/env python
from a1 import *
from sys import argv, exit

if __name__ == "__main__":
    argc = len(argv)
    if argc != 2:
        print "Usage: divideandconquer.py input_file"
        exit()

    filepath = argv[1]
    data = read_input()

    output = naive(data)
    print output[0]
    for pair1, pair2 in output[1]:
        print pair1, pair2


