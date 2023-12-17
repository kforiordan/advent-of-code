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



def energise(tiles, mirrors, origin, direction, energised = None, depth=0):
    if depth > 500:
        print("Bailing out")
        return False

    (y,x) = origin[0]+direction[0], origin[1]+direction[1]

    in_bounds = lambda l,w: l>=0 and l<len(tiles) and w>=0 and w<len(tiles[0])

    if not in_bounds(y,x):
        return False

    if energised == None:
        energised = {}

    if (y,x) in energised:
        if origin in energised[(y,x)]:
            energised[(y,x)][origin] += 1
            return True
        else:
            energised[(y,x)][origin] = 1
    else:
        energised[(y,x)] = {origin: 1}
#        print("{} -> {}    ({})".format(origin, direction, energised))

    # Raw backslash breaks emacs python mode's indentation and highlighting.
    mirror_string = "".join(['-', '|', '/', chr(92)])
    t = tiles[y][x]
    directions = [direction]
    if t in mirror_string:
        if t == '-':
            if origin[0] != y:
                directions = [(0,-1), (0,1)]
        elif t == '|':
            if origin[1] != x:
                directions = [(-1,0), (1,0)]
        elif t == '/':
            if origin[0] < y:
                directions = [(0,-1)]
            elif origin[0] > y:
                directions = [(0,1)]
            elif origin[1] < x:
                directions = [(-1,0)]
            elif origin[1] > x:
                directions = [(1,0)]
            else:
                directions = None
        elif t == chr(92):
            if origin[0] < y:
                directions = [(0,1)]
            elif origin[0] > y:
                directions = [(0,-1)]
            elif origin[1] < x:
                directions = [(1,0)]
            elif origin[1] > x:
                directions = [(-1,0)]
            else:
                directions = None

    if directions == None:
        print("Exiting: {}: {} -> {}".format(t, origin, (y,x)))
        exit(0)

    for d in directions:
        energise(tiles, mirrors, (y,x), d, energised, depth+1)

    return energised

def print_solution(tiles, energised):
    s = None
    for y,row in enumerate(tiles):
        s = []
        for x,t in enumerate(row):
            if (y,x) in energised:
                s.append('#')
            else:
                s.append(t)
        print("".join(s))


if __name__ == "__main__":
    tiles, mirrors = get_tiles(sys.stdin)
    start = (0,-1)
    next_step = (0,1) # Moving to the right; add to current position.
    energised = energise(tiles, mirrors, start, (0,1))
    paths_seen = {}
    print("Silver: {}".format(len(energised.keys())))
    print_solution(tiles, energised)


