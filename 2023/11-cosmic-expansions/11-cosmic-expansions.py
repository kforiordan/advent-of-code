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
        i = 0
        offset = 0
        z = len(galaxy_count)
        while i < z:
            if galaxy_count[i] == 0:
                row.insert(i+offset, '.')
                offset += 1
            i += 1

    return expanded


def manhattan(a, b):
    (ay, ax) = a
    (by, bx) = b
    ydist = abs(by - ay)
    xdist = abs(bx - ax)
    return ydist + xdist


def get_galaxies(u):
    coords = []
    for y,row in enumerate(u):
        for x,cell in enumerate(row):
            if cell == '#':
                coords.append((y,x))
    return coords


def get_path_distances(coords):
    path_distances = {g:[] for g in coords}
    for i,g in enumerate(coords):
        j = i+1
        while j < len(coords):
            path_distances[g].append(manhattan(g, coords[j]))
            j += 1
    return path_distances


if __name__ == "__main__":
    universe = get_raw_universe(sys.stdin)
    expanded_universe = expand_universe(universe)
    galaxy_coords = get_galaxies(expanded_universe)
    path_distances = get_path_distances(galaxy_coords)

    print("Silver: {}".format(sum(list(map(sum,list(path_distances.values()))))))
