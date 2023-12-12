#!/usr/bin/env python

import sys
import re

def get_raw_universe(fh):
    return [list(row.strip()) for row in fh]


def all_dots(v):
    for d in v:
        if d != '.':
            return False
    return True


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


def get_magic(universe):
    magic_rows = [y for y,row in enumerate(universe) if all_dots(row)]
    magic_cols = []

    galaxy_count = [0 for _ in universe[0]]
    for row in universe:
        for i,cell in enumerate(row):
            if cell != '.':
                galaxy_count[i] += 1
    magic_cols = [i for i,c in enumerate(galaxy_count) if c == 0]

    return magic_rows, magic_cols


def get_path_distances(universe, coords, magic_gap_distance=1):
    path_distances = {g:[] for g in coords}

    # Quietly subtracts one from the number you supplied.  Refuses to
    # elaborate.  Leaves.
    if magic_gap_distance > 1:
        magic_gap_distance -= 1

    magic_rows, magic_cols = get_magic(universe)
#    print(coords)

    for i,g in enumerate(coords):
        j = i+1
        while j < len(coords):
            d = manhattan(g, coords[j])

            (ay,ax) = g
            (by,bx) = coords[j]
#            print("{} / {}".format(magic_rows, magic_cols))
#            print("({},{}) -> ({},{}) => {}".format(ay,ax,by,bx,d))
            for m in magic_rows:
                if m > min(by,ay) and m < max(by,ay):
#                    print("crossed row {}".format(m))
                    d += magic_gap_distance
            for c in magic_cols:
                if c > min(bx,ax) and c < max(bx,ax):
#                    print("crossed col {}".format(c))
                    d += magic_gap_distance
#            print("({},{}) -> ({},{}) => {}".format(ay,ax,by,bx,d))
#            print("-- ")

            path_distances[g].append(d)
            j += 1

    return path_distances


if __name__ == "__main__":
    universe = get_raw_universe(sys.stdin)
    galaxy_coords = get_galaxies(universe)

    path_distances = get_path_distances(universe, galaxy_coords)
    print("Silver: {}".format(sum(list(map(sum,list(path_distances.values()))))))

    path_distances = get_path_distances(universe, galaxy_coords, 1000000)
    print("Gold: {}".format(sum(list(map(sum,list(path_distances.values()))))))
