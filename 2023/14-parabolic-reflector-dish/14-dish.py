#!/usr/bin/env python3

import sys

def get_platform(fh):
    return [list(row.rstrip()) for row in fh]


def print_platform(p):
    for row in p:
        print("".join(row))


def tilt(platform):
    empty_space, static_rock, rolling_rock = '.', '#', 'O'
    northmost_empty = [None for _ in platform[0]]
    for y,row in enumerate(platform):
        # print("NME: {}".format(northmost_empty))
        # print("Pla: {}".format(row))
        for x,cell in enumerate(row):
            if cell == empty_space:
                if northmost_empty[x] == None:
                    northmost_empty[x] = y
            elif cell == static_rock:
                northmost_empty[x] = None
            elif cell == rolling_rock:
                if northmost_empty[x] == None:
                    continue
                else:
                    # Move this rolling rock to the next available empty slot.
                    platform[northmost_empty[x]][x] = cell
                    # print("x: {}".format(x))
                    # print("nme_x: {}".format(northmost_empty[x]))
                    # print("cell: {}".format(cell))
                    # print("after: {}".format(platform[northmost_empty[x]][x]))
                    platform[y][x] = empty_space
                    northmost_empty[x] = northmost_empty[x] + 1

#        print("NME: {}".format(northmost_empty))
        # if y == 1:
        #     print("Pla: {}".format(platform[0]))
        # print("Pla: {}".format(row))
        # print("-- ")
    return platform


def stupid_sum(platform):
    empty_space, static_rock, rolling_rock = '.', '#', 'O'
    stupid = 0
    for y,row in enumerate(platform):
        for x,cell in enumerate(row):
            if cell == rolling_rock:
                stupid += len(platform) - y
    return stupid

if __name__ == "__main__":
    platform = get_platform(sys.stdin)
    # print_platform(platform)
    # print("-- ")
    tilted_platform = tilt(platform)
    # print_platform(tilted_platform)
    # print("-- ")
    print("Silver: {}".format(stupid_sum(platform)))
