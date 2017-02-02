#!/usr/bin/env python
from a1 import *
import timeit
from random import randint
from copy import deepcopy

TIME_BRUTE_FORCE = True
TIME_NAIVE = False
TIME_ENHANCED = False

brute_force_times = []
naive_times = []
enhanced_times = []


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def print_results():
    if TIME_BRUTE_FORCE:
        print "Brute Force Times:"
        for n, time in brute_force_times:
            print n, time

    if TIME_NAIVE:
        print "Naive Times:"
        for n, time in naive_times:
            print n, time

    if TIME_ENHANCED:
        print "Enhanced Times:"
        for n, time in enhanced_times:
            print n, time


if __name__ == "__main__":
    try:
        for i in range(1, 7):
            data = []
            print "Building data set"
            for j in range(0, pow(10, i)):
                x = randint(0, 65535)
                y = randint(0, 65535)
                data.append((x, y))

            n = len(data)
            print "Running trial", i, "with n", n

            if TIME_BRUTE_FORCE:
                wrapped = wrapper(brute_force, data)
                brute_force_times.append((n, timeit.timeit(wrapped, number=1)))

            if TIME_NAIVE:
                data_x = deepcopy(data)
                mergeSort(data_x, 0)

                wrapped = wrapper(naive, data_x)
                naive_times.append((n, timeit.timeit(wrapped, number=1)))

            if TIME_ENHANCED:
                data_x = deepcopy(data)
                data_y = deepcopy(data)
                mergeSort(data_x, 0)
                mergeSort(data_y, 1)

                wrapped = wrapper(enhanced, data_x, data_y)
                enhanced_times.append((n, timeit.timeit(wrapped, number=1)))

            print "Done."

        print_results()

    except (KeyboardInterrupt, MemoryError) as e:
        print e
        print_results()
