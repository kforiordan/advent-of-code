import sys
import pprint


def get_map(fh):
    return [list(line.strip()) for line in fh]


def adjacent(cave_map, path, p):
    x, y = p
    min_y = 0
    min_x = 0
    max_y = len(cave_map) - 1
    max_x = len(cave_map[0]) - 1
    y_bound = lambda a: a >= min_y and a <= max_y
    x_bound = lambda a: a >= min_x and a <= max_x

    return [(x2,y2) for (x2,y2) in [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]
            if x_bound(x2) and y_bound(y2)]


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()

    # I initially called this variable 'map', which is allowed, but is
    # a terrible idea.  I didn't even notice the syntax highlight.

    cave_map = get_map(sys.stdin)
