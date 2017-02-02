#!/usr/bin/env python
from a1 import *
import timeit
from random import randint

TIME_BRUTE_FORCE = False
TIME_NAIVE = True
TIME_ENHANCED = True

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

            data_x = data
            data_y = data_x

            mergeSort(data_x, 0)
            mergeSort(data_y, 1)

            if TIME_BRUTE_FORCE:
                wrapped = wrapper(brute_force, data)
                brute_force_times.append((n, timeit.timeit(wrapped, number=1)))

            if TIME_NAIVE:
                wrapped = wrapper(naive, data_x)
                naive_times.append((n, timeit.timeit(wrapped, number=1)))

            if TIME_ENHANCED:
                wrapped = wrapper(enhanced, data_x, data_y)
                enhanced_times.append((n, timeit.timeit(wrapped, number=1)))

            print "Done."

        print_results()

    except KeyboardInterrupt:
        print_results()
