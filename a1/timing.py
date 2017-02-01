#!/usr/bin/env python
from a1 import *
import timeit
from random import randint


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


if __name__ == "__main__":
    brute_force_times = []
    naive_times = []
    enhanced_times = []

    for i in range(1, 5):
        data = []
        for j in range(0, pow(10, i)):
            while True:
                x = randint(1, 1000)
                y = randint(1, 1000)
                if (x, y) not in data:
                    data.append((x, y))
                    break

        n = len(data)
        print "Running trial", i, "with n", n

        wrapped = wrapper(brute_force, data)
        brute_force_times.append((n, timeit.timeit(wrapped, number=1)))

        wrapped = wrapper(naive, data)
        naive_times.append((n, timeit.timeit(wrapped, number=1)))

        wrapped = wrapper(enhanced, data)
        enhanced_times.append((n, timeit.timeit(wrapped, number=1)))

    print "Brute Force Times:"
    for n, time in brute_force_times:
        print n, time

    print "Naive Times:"
    for n, time in naive_times:
        print n, time

    print "Enhanced Times:"
    for n, time in enhanced_times:
        print n, time