#!/usr/bin/env python

import sys
import re

def get_raw_universe(fh):
    return [list(row.strip()) for row in fh]


def expand_universe(u):
    expanded = []

    def all_dots(v):
        for d in v:
            if d != '.':
                return False
        return True

    # Expand rows
    for row in u:
        if all_dots(row):
            expanded.append(['.' for _ in u[0]])
        expanded.append(row)

    # Expand columns
    galaxy_count = [0 for _ in u[0]]
    for row in u:
        for i,cell in enumerate(row):
            if cell != '.':
                galaxy_count[i] += 1
    for row in expanded:
        for i,n in enumerate(galaxy_count):
            if n == 0:
                row.insert(i, '.')

    return expanded


if __name__ == "__main__":
    universe = get_raw_universe(sys.stdin)
    expanded_universe = expand_universe(universe)
