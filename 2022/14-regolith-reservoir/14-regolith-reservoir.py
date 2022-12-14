#!/usr/bin/env python

import sys

# Test input looks like:
#498,4 -> 498,6 -> 496,6
#503,4 -> 502,4 -> 502,9 -> 494,9
def get_barriers(fh):
    barrier_points = []

    for line in fh:
        l2d = lambda xy: {"x":int(xy[0]), "y":int(xy[1])}
        points = list(map(lambda p: l2d(p.split(",")), line.rstrip('\n').split(' -> ')))
        barrier_points.append(points)

    return barrier_points


def is_empty(point):
    # First check if there's a barrier in the way
    return True


def is_falling_into_the_endless_void(sand):
    return True
    sand["y"] > max_y or sand["x"] < min_x or sand["x"] > max_x


def fall_once(sand):
    # "A unit of sand always falls down one step if possible. If the
    # tile immediately below is blocked (by rock or sand), the unit of
    # sand attempts to instead move diagonally one step down and to
    # the left. If that tile is blocked, the unit of sand attempts to
    # instead move diagonally one step down and to the right."
    down = {"y": sand["y"]+1, "x": sand["x"]}
    downleft = {"y": sand["y"]+1, "x": sand["x"]-1}
    downright = {"y": sand["y"]+1, "x": sand["x"]+1}
    for n in [down, downleft, downright]:
        if is_empty(n):
            return n
    return sand


def fall(sand):
    pos = fall_once(sand)
    if pos == sand:
        # Falling was blocked by something.
        return pos
    elif is_falling_into_the_endless_void(pos):
        return None
    return fall(pos)


if __name__ == "__main__":
    barrier_points = get_barriers(sys.stdin)

    max_y = max([p["y"] for ps in barrier_points for p in ps])
    min_x = min([p["x"] for ps in barrier_points for p in ps])
    max_x = max([p["x"] for ps in barrier_points for p in ps])
    #print("{} {} {}".format(max_y, min_x, max_x))

    #print(barrier_points)

    sand_start = {"y":0, "x":500}
    sand_points = []

    rest = fall(sand_start)
    while rest != None:
        sand_points.append(rest)
        fall(sand_start)

    print("Silver: {}".format(len(sand_points)))
