#!/usr/bin/env python3

import sys

def get_platform(fh):
    return [list(row.rstrip()) for row in fh]


def print_platform(p):
    for row in p:
        print("".join(row))


def tilt_north(platform):
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


# Borrowing transpose & rotate90 from day 13's puzzle, which I solved on day 22.

# https://stackoverflow.com/questions/52342209/matrix-transpose-without-numpy-error-list-index-out-of-range
#
# Another suggestion on that page, list(zip(*pattern)), returns a list
# of tuples.
#
def transpose(pattern):
    return list(map(list, zip(*pattern)))


# Building on the above transpose
def rotate_90(pattern):
    return [list(reversed(row)) for row in transpose(pattern)]


# This is so stupid
def rotate_minus_90(p):
    return rotate_90(rotate_90(rotate_90(p)))


# I can't remember much about hashing. .. Hmm, that's not good enough.
# I had to do a little reading, and what I was struggling to remember
# was 'a polynomial rolling hash function'.  I don't have time to read
# the whole thing so let's just do a stupid implementation.
def stupid_hash(platform):
    stupid = 0
    stupid_prime = 29
    stupid_m = 100000
    stupid_correspondence = {'.': 3,
                             '#': 7,
                             'O': 11,}

    rolling_p = 1
    for y,row in enumerate(platform):
        for x,cell in enumerate(row):
            stupid += stupid_correspondence[cell] * rolling_p
            rolling_p = rolling_p * stupid_prime

    return stupid % stupid_m



def cycle(platform):
    p = platform

    # Start by tilting
    p = tilt_north(p)

    # Now west becomes north, so we can reuse tilt_north
    p = rotate_90(p)
    p = tilt_north(p)

    # South -> west -> north
    p = rotate_90(p)
    p = tilt_north(p)

    # East -> south -> west -> north
    p = rotate_90(p)
    p = tilt_north(p)

    # Back to the starting orientation
    p = rotate_90(p)

    return p


if __name__ == "__main__":
    platform = get_platform(sys.stdin)
    # print_platform(platform)
    # print("-- ")
    if (False):
        tilted_platform = tilt_north(platform)
        # print_platform(tilted_platform)
        # print("-- ")
        print("Silver: {}".format(stupid_sum(platform)))

    p = platform
    print_platform(p)
    print("----------------")
    p = cycle(p)
    print_platform(p)

