#!/usr/bin/env python3

import sys
from functools import reduce


def get_grid(fh):
    return [list(map(int,line.strip())) for line in fh]


if __name__ == "__main__":
    grid = get_grid(sys.stdin)

    n_rows = len(grid)
    n_cols = len(grid[0])

    is_edge = lambda y, x: y == 0 or y == n_rows-1 or x == 0 or x == n_cols-1
    above = lambda y, x: reversed([(y,x) for y in range(0, y)])
    below = lambda y, x: [(y,x) for y in range(y+1, n_rows)]
    left = lambda y, x: reversed([(y,x) for x in range(0, x)])
    right = lambda y, x: [(y,x) for x in range(x+1, n_cols)]
    val = lambda y, x: grid[y][x]
    vals = lambda coords: [val(y,x) for (y,x) in coords]

    def visible(row, col):
        if is_edge(row, col):
            return True
        else:
            # "A tree is visible if all of the other trees between it
            # and an edge of the grid are shorter than it"
            height = val(row, col)
            visible_directions = []
            for direction in [above, below, left, right]:
                tree_heights = vals(direction(row, col))
                shorter = lambda hs: list(map(lambda x: x < height, hs))
                visible_directions.append(reduce(lambda a, b: a and b, shorter(tree_heights), True))
        return reduce(lambda a, b: a or b, visible_directions, False)

    n_visible_from_outside = 0
    # range should be narrower, as there's no point in checking the edges.
    for row in range(0, n_rows):
        for col in range(0, n_cols):
            if visible(row, col):
                n_visible_from_outside += 1

    def n_trees_visible(row, col):
        n_visible_in_each = []
        for direction in [above, left, below, right]:
            n = 0
            trees = direction(row, col)
            for tree in trees:
                (y, x) = tree
                if val(y, x) < val(row, col):
                    n += 1
                elif val(y, x) >= val(row, col):
                    n += 1
                    break
            n_visible_in_each.append(n)
        return n_visible_in_each

    score = lambda row, col: reduce(lambda a, b: a * b, n_trees_visible(row, col), 1)
    # I shouldn't check the edges here either, but consistency of
    # incorrectness is important.
    scores = [score(row, col) for row in range(0, n_rows) for col in range(0, n_cols)]

    print("Silver: {}".format(n_visible_from_outside))
    print("Gold: {}".format(sorted(scores)[-1]))
