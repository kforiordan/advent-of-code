#!/usr/bin/env python3

import sys


# returns True if a1 overlaps a2
def overlaps(assignment1, assignment2):
    (a1a, a1z), (a2a, a2z) = assignment1, assignment2
    return (a1a >= a2a and a1a <= a2z) or (a1z >= a2a and a1z <= a2z)


# returns True if a1 fully contains a2
def contains(assignment1, assignment2):
    (a1a, a1z), (a2a, a2z) = assignment1, assignment2
    return a1a <= a2a and a1z >= a2z


# Reads lists of chars from fh, returns list of tuples of tuples ...
def get_assignments(fh):
    assignments = []

    for line in fh:
        line = line.rstrip('\n')
        a1,a2 = map(lambda a: tuple(map(int, a.split("-"))), line.split(","))
        assignments.append((a1,a2))

    return assignments


if __name__ == "__main__":
    assignments = get_assignments(sys.stdin)

    silver_n = 0
    gold_n = 0
    for (a1,a2) in assignments:
        if contains(a1, a2) or contains(a2, a1):
            silver_n += 1
        if contains(a1, a2) or overlaps(a1, a2):
            gold_n += 1

    print(f'Silver: {silver_n}')
    print(f'Gold: {gold_n}')
