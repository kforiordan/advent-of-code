#!/usr/bin/env python3

import sys
from functools import reduce


def get_grid(fh):
    return [list(map(int,line.strip())) for line in fh]


if __name__ == "__main__":
    grid = get_grid(sys.stdin)

    n_rows = len(grid)
    n_cols = len(grid[0])

    def visible(row, col):
        is_edge = lambda y, x: y == 0 or y == n_rows-1 or x == 0 or x == n_cols-1
        above = lambda y, x: [(y,x) for y in range(0, y)]
        below = lambda y, x: [(y,x) for y in range(y+1, n_rows)]
        left = lambda y, x: [(y,x) for x in range(0, x)]
        right = lambda y, x: [(y,x) for x in range(x+1, n_cols)]
        val = lambda y, x: grid[y][x]
        vals = lambda coords: [val(y,x) for (y,x) in coords]

        if is_edge(row, col):
            return True
        else:
            # "A tree is visible if all of the other trees between it
            # and an edge of the grid are shorter than it"
            #
            height = val(row, col)
            visible_directions = []
            for direction in [above, below, left, right]:
                tree_heights = vals(direction(row, col))
                shorter = lambda hs: list(map(lambda x: x < height, hs))
                visible_directions.append(reduce(lambda a, b: a and b, shorter(tree_heights), True))
        return reduce(lambda a, b: a or b, visible_directions, False)

    n_visible = 0
    for row in range(0, n_rows):
        for col in range(0, n_cols):
            if visible(row, col):
                n_visible += 1

    print("Silver: {}".format(n_visible))

