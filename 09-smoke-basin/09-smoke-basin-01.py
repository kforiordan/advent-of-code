
import sys
import pprint
from functools import reduce


def get_heightmap(fh):
    heightmap = []

    for line in fh:
        h = list(map(int,list(line.strip())))
        heightmap.append(h)

    return heightmap


def adjacent_points(heightmap, x, y):
    (min_y, max_y) = 0, len(heightmap) - 1
    (min_x, max_x) = 0, len(heightmap[0]) - 1

    pm = lambda a: [a-1, a, a+1]
    y_bound = lambda a: a >= min_y and a <= max_y
    x_bound = lambda a: a >= min_x and a <= max_x

    adjacent_points = [ (x2,y2) for y2 in pm(y) if 1 for x2 in pm(x) \
                        if (x2,y2) != (x,y) and y_bound(y2) and x_bound(x2)]

    return adjacent_points


def adjacent_values(heightmap, x, y):
    return([heightmap[y2][x2] for (x2,y2) in adjacent_points(heightmap, x, y)])


def lowerthanall(one, others):
    return reduce(lambda x, y: x and y, [one < v for v in others], True)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)

    heightmap = get_heightmap(sys.stdin)
    risk_sum = 0
    for y in range(0, len(heightmap)):
        for x in range(0, len(heightmap[0])):
            if lowerthanall(heightmap[y][x], adjacent_values(heightmap, x, y)):
                risk_sum += 1 + heightmap[y][x]

    print("Risk sum: {}".format(risk_sum))
