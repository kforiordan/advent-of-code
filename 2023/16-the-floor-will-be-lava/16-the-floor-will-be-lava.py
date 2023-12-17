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



def energise(tiles, origin, direction, energised = None, depth=0):
    if depth > 500:
        print("Bailing out")
        return False

    if energised == None:
        energised = {}

    in_bounds = lambda l,w: l>=0 and l<len(tiles) and w>=0 and w<len(tiles[0])

    mirror_string = "".join(['-', '|', '/', chr(92)])

    oy,ox = origin
    dy,dx = direction
    ny,nx = oy+dy, ox+dx
    stupid_stack = [{'from':(oy,ox), 'to':(ny,nx)}]
    while len(stupid_stack) > 0:
        step = stupid_stack.pop()

        from_y, from_x = step['from'][0], step['from'][1]
        to_y, to_x = step['to'][0], step['to'][1]

        if not in_bounds(to_y, to_x):
            continue

        if (to_y, to_x) in energised:
            if (from_y, from_x) in energised[(to_y, to_x)]:
                energised[(to_y, to_x)][(from_y, from_x)] += 1
                continue
            else:
                energised[(to_y, to_x)][(from_y, from_x)] = 1
        else:
            energised[(to_y, to_x)] = {(from_y, from_x): 1}


#        print("{}: {} -> {}    ({})".format(depth, (from_y, from_x), (to_y, to_x), energised))

        default_direction = (to_y-from_y, to_x-from_x)
        directions = [default_direction]
        t = tiles[to_y][to_x]
        if t in mirror_string:
            if t == '-':
                if from_y != to_y:
                    directions = [(0,-1), (0,1)]
            elif t == '|':
                if from_x != to_x:
                    directions = [(-1,0), (1,0)]
            elif t == '/':
                if from_y < to_y:
                    directions = [(0,-1)]
                elif from_y > to_y:
                    directions = [(0,1)]
                elif from_x < to_x:
                    directions = [(-1,0)]
                elif from_x > to_x:
                    directions = [(1,0)]
                else:
                    directions = None
            elif t == chr(92):
                if from_y < to_y:
                    directions = [(0,1)]
                elif from_y > to_y:
                    directions = [(0,-1)]
                elif from_x < to_x:
                    directions = [(1,0)]
                elif from_x > to_x:
                    directions = [(-1,0)]
                else:
                    directions = None

        if directions == None:
            print("Exiting: {}: {} -> {}".format(t, (from_y, from_x), (to_y,to_x)))
            exit(0)

        for d in directions:
            stupid_stack.append({'from':(to_y, to_x), 'to':(to_y+d[0], to_x+d[1])})

    return energised


def print_tiles(tiles, energised, mark = None):
    s = None
    for y,row in enumerate(tiles):
        s = []
        for x,t in enumerate(row):
            if (y,x) in energised:
                if mark == None:
                    s.append(t)
                else:
                    s.append('#')
            else:
                s.append(t)
        print("".join(s))


if __name__ == "__main__":
    tiles, mirrors = get_tiles(sys.stdin)
    start = (0,-1)
    next_step = (0,1) # Moving to the right; add to current position.
    energised = energise(tiles, start, (0,1))
    paths_seen = {}
    print("Silver: {}".format(len(energised.keys())))
#    print_tiles(tiles, energised, '#')


