#!/usr/bin/env python3

# Counting groups of numbers.

# Generalised a bit: we want the sum of the largest three numbers now.

import sys
# python's heapq implements a min heap, but we want a max heap.
import heapq

if __name__ == "__main__":
    cals = -1
    max_cals = cals
    inv = []

    for line in sys.stdin:
        line = line.strip()
        if line == "":
            if cals != -1:
                # Negating the values we store, because of the min-heap thing.
                heapq.heappush(inv, -cals)
                if cals > max_cals:
                    max_cals = cals
                cals = -1
        else:
            if cals == -1:
                cals = int(line)
            else:
                cals += int(line)

    # Negating the values we pop, ...
    print(-(heapq.heappop(inv) + heapq.heappop(inv) + heapq.heappop(inv)))

