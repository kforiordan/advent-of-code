#!/usr/bin/env python

import sys

# Test input looks like:
#   498,4 -> 498,6 -> 496,6
#   503,4 -> 502,4 -> 502,9 -> 494,9
#
# returns: [ [{x:498, y:4}, {x:498, y:6}, {x:496, y:6}], [{x:503, y:4}, ...] ]
#
def get_barriers(fh):
    barrier_points = []

    for line in fh:
        l2d = lambda xy: {"x":int(xy[0]), "y":int(xy[1])}
        points = list(map(lambda p: l2d(p.split(",")), line.rstrip('\n').split(' -> ')))
        barrier_points.append(points)

    return barrier_points


# given a line (a tuple of two points, a & b) and a point
# returns True if point is on line, else False.
def is_on(line, point):
    (a, b) = line
    if a["y"] == b["y"] and point["y"] == a["y"]:
        if point["x"] >= min([a["x"],b["x"]]) and point["x"] <= max([a["x"],b["x"]]):
            return True
    elif a["x"] == b["x"] and point["x"] == a["x"]:
        if point["y"] >= min([a["y"],b["y"]]) and point["y"] <= max([a["y"],b["y"]]):
            return True
    return False


def is_empty(point):
    # First check if there's a barrier in the way
    for b in barriers:
        prev_p = None
        for p in b:
            if prev_p != None:
                if is_on((prev_p, p), point):
                    return False
            prev_p = p

    # Now check if there's sand already at this point
    for p in sand_points:
        if point["y"] == p["y"] and point["x"] == p["x"]:
            return False

    return True


def is_falling_into_the_endless_void(sand):
    return sand["y"] > max_y or sand["x"] < min_x or sand["x"] > max_x


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
    if pos["y"] == sand["y"] and pos["x"] == sand["x"]:
        # Falling was blocked by something.
        return pos
    elif is_falling_into_the_endless_void(pos):
        return None
    return fall(pos)


if __name__ == "__main__":
    barriers = get_barriers(sys.stdin)

    max_y = max([p["y"] for ps in barriers for p in ps])
    min_x = min([p["x"] for ps in barriers for p in ps])
    max_x = max([p["x"] for ps in barriers for p in ps])

    sand_start = {"y":0, "x":500}
    sand_points = []

    rest = fall(sand_start)
    while rest != None:
        sand_points.append(rest)
        rest = fall(sand_start)

    print("Silver: {}".format(len(sand_points)))
