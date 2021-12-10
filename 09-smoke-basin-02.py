
import sys
import pprint
from functools import reduce
import operator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    v: int

    def __hash__(self):
        return hash('{},{}'.format(self.x, self.y))

    # Should I compare value (v) too?  Idk.  No use case right now.
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and \
                self.x == other.x and \
                self.y == other.y)


def get_height_map(fh):
    height_map = []

    for line in fh:
        h = list(map(int,list(line.strip())))
        height_map.append(h)

    return height_map


def adjacent_points(height_map, x, y):
    (min_y, max_y) = 0, len(height_map) - 1
    (min_x, max_x) = 0, len(height_map[y]) - 1

    y_bound = lambda a: a >= min_y and a <= max_y
    x_bound = lambda a: a >= min_x and a <= max_x

    up, down, left, right = [], [], [], []

    for y2 in range(y-1, min_y-1, -1):
        if y_bound(y2) and x_bound(x) and \
           height_map[y2][x] != magic_basin_border:
            up.append((x, y2))
        else:
            break

    for y2 in range(y+1, max_y+1):
        if y_bound(y2) and x_bound(x) and \
           height_map[y2][x] != magic_basin_border:
            down.append((x, y2))
        else:
            break

    for x2 in range(x-1, min_x-1, -1):
        if y_bound(y) and x_bound(x2) and \
           height_map[y][x2] != magic_basin_border:
            left.append((x2, y))
        else:
            break

    for x2 in range(x+1, max_x+1):
        if y_bound(y) and x_bound(x2) and \
           height_map[y][x2] != magic_basin_border:
            right.append((x2, y))
        else:
            break

    adjacent = up + down + left + right

    return adjacent


# Imperative recursion, oh man, I hate this.
def explore(height_map, point_to_basin_map, points):
    for (x,y) in points:
        p = Point(x, y, height_map[y][x])
        if p.v == magic_basin_border:
            continue
        elif p in point_to_basin_map:
            continue
        else:
            point_to_basin_map[p] = basin_i
            explore(height_map, point_to_basin_map,
                    adjacent_points(height_map, x, y))


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)

    magic_basin_border = 9
    height_map = get_height_map(sys.stdin)
    point_to_basin_map = {}
    basin_to_point_map = []

    basin_i = 0
    for y in range(0, len(height_map)):
        for x in range(0, len(height_map[y])):
            p = Point(x, y, height_map[y][x])
            if p not in point_to_basin_map and p.v != magic_basin_border:
                point_to_basin_map[p] = basin_i
                explore(height_map, point_to_basin_map,
                        adjacent_points(height_map, x, y))
                basin_i += 1

    basin_to_point_map = [[] for x in
                          range(0, max(point_to_basin_map.values()) + 1)]
    for p in point_to_basin_map:
        basin_to_point_map[point_to_basin_map[p]].append(p)

    basin_sizes = map(len, basin_to_point_map)
    top_three = (list(reversed(sorted(basin_sizes))))[0:3]

    pp.pprint(reduce(operator.mul,top_three,1))
