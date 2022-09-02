import numpy as np
import time


def comprehension_way(n):
    start = time.perf_counter()
    d = [
        sum(j + i + k for k in range(10))
        for i in range(n)
        for j in range(n)
    ]
    end = time.perf_counter()

    return d, end - start


def non_comprehension_way(n):
    start = time.perf_counter()
    c = []
    for i in range(n):
        for j in range(n):
            d = sum(j + i + k for k in range(10))
            c.append(d)

    end = time.perf_counter()

    return c, end - start


def the_worst_way(n):
    start = time.perf_counter()
    c = []
    for i in range(n):
        for j in range(n):
            d = 0
            for k in range(10):
                d += j + i + k
            c.append(d)

    end = time.perf_counter()

    return c, end - start


# n = 5000
#
# dd, diff1 = comprehension_way(n)
# print(f"Comp for {n} elements time is: {diff1}")
#
# vv, diff2 = non_comprehension_way(n)
# print(f"NonComp for {n} elements time is: {diff2}")
#
# cc, diff3 = the_worst_way(n)
# print(f"NonComp for {n} elements time is: {diff3}")
#
# print()
# print(f"Comp compared to non-comp: {diff1/diff2}")
#
# print(f"For compared to non-comp: {diff3/diff2}")
# print()
# print(len(vv))
# print(len(cc))
#
# print(dd[:20])
# print(vv[:20])
# print(cc[:20])


start = time.time()
time.sleep(0.001)
end = time.time()
print(end-start)

start = time.perf_counter()
time.sleep(0.001)
end = time.perf_counter()
print(end-start)


