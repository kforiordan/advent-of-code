#!/usr/bin/env python3

import sys


def get_tiles(fh):
    tiles = [list(line.rstrip()) for line in fh]
    mirrors = []

    # Raw backslash breaks emacs python mode's indentation and highlighting.
    mirror_string = "".join(list(map(chr,[45,47,92,124])))
    for y,row in enumerate(tiles):
        for x,cell in enumerate(row):
            if cell in mirror_string:
                mirrors.append((y,x))

    return tiles, mirrors



def energise(tiles, mirrors, origin, direction, energised = None):
    (y,x) = origin[0]+direction[0], origin[1]+direction[1]
    mirror_string = "".join(list(map(chr,[45,47,92,124])))

    in_bounds = lambda y,x: if y>=0 and y<len(tiles) and \
        x>=0 and x<len(tiles[0])
    if not in_bounds(y,x):
        return False

    if energised == None:
        energised = {}

    # oh python mode
    if tiles[y][x] in mirror_string:
        fjdsoifj
    else:
        energise(tiles, mirrors, (y,x), direction, energised))



    return energised


if __name__ == "__main__":
    tiles, mirrors = get_tiles(sys.stdin)
    start = (0,-1)
    next_step = (0,1) # Moving to the right; add to current position.
    energised = energise(tiles, mirrors, start, (0,1))
    paths_seen = {}
