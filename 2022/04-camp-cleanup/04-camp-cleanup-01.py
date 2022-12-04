#!/usr/bin/env python3

from functools import reduce

import sys

# Reads lists of chars from fh, returns list of tuples, each tuple
# containing half of a list of chars.
def get_assignments(fh):
    assignments = []

    for line in fh:
        a1,a2 = map(lambda a: tuple(a.split("-")), line.split(","))
        assignments.append((a1,a2))

    return assignments


if __name__ == "__main__":
    assignments = get_assignments(sys.stdin)

    silver = len(assignments)
    print(f'Silver: {silver}')
