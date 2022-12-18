#!/usr/bin/env python3

import sys
import pprint

def get_boulders(fh):
    return [list(map(int,line.rstrip('\n').split(','))) for line in fh]

def adjacent_points(x,y,z):
    return [[x-1,y,z],[x+1,y,z],[x,y-1,z],[x,y+1,z],[x,y,z-1],[x,y,z+1]]

def has_boulder(x,y,z):
    return boulders3d[x][y][z]

if __name__ == "__main__":
    boulders = get_boulders(sys.stdin)

    max_x = max(map(lambda a: a[0], boulders))
    max_y = max(map(lambda a: a[1], boulders))
    max_z = max(map(lambda a: a[2], boulders))

    boulders3d = [[[False for _ in range(0, max_z+2)] for _ in range(0, max_y+2)] for _ in range(0, max_z+2)]

    for b in boulders:
        x,y,z = b
        boulders3d[x][y][z] = True
        b.append(6)

    for boulder in boulders:
        x,y,z,f = boulder
        for point in adjacent_points(x,y,z):
            px,py,pz = point
            if has_boulder(px,py,pz):
                boulder[-1] -= 1

    pp = pprint.PrettyPrinter()
    silver = 0
    for x,y,z,f in boulders:
        silver += f

    print("Silver {}".format(silver))
