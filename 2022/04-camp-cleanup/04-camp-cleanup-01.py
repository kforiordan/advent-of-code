#!/usr/bin/env python3

from functools import reduce

import sys

# returns True if a1 fully contains a2
def contains(assignment1, assignment2):
    (a1a, a1z), (a2a, a2z) = assignment1, assignment2
    return a1a <= a2a and a1z >= a2z

# Reads lists of chars from fh, returns list of tuples, each tuple
# containing half of a list of chars.
def get_assignments(fh):
    assignments = []

    for line in fh:
        line = line.rstrip('\n')
        a1,a2 = map(lambda a: tuple(map(int, a.split("-"))), line.split(","))
        assignments.append((a1,a2))

    return assignments


if __name__ == "__main__":
    assignments = get_assignments(sys.stdin)

    n = 0
    for (a1,a2) in assignments:
        if contains(a1, a2) or contains(a2, a1):
            n += 1

    print(f'Silver: {n}')
