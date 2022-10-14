import sys
import pprint


class Point:
    x: int
    y: int
    v: int

    def __init__(self, x, y, v):
        self.x = int(x)
        self.y = int(y)
        self.v = int(v)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.x == other.x and self.y == other.y)

    def __hash__(self):
        return hash('{},{}'.format(self.x, self.y))

    def __str__(self):
        return("({},{}) -> {}".format(self.x, self.y, self.v))

    def __repr__(self):
        return("Point({}, {}, {})".format(self.x, self.y, self.v))


def get_map(fh):
    ys = []
    for y,line in enumerate(fh):
        xs = []
        for x,v in enumerate(list(line.strip())):
            xs.append(Point(x,y,v))
        ys.append(xs)
    return(ys)


def adjacent(cave_map, p):
    min_y = 0
    min_x = 0
    max_y = len(cave_map) - 1
    max_x = len(cave_map[0]) - 1
    # y_bound = lambda p: p.y >= min_y and p.y <= max_y
    # x_bound = lambda p: p.x >= min_x and p.x <= max_x
    y_bound = lambda y: y >= min_y and y <= max_y
    x_bound = lambda x: x >= min_x and x <= max_x

    nsew = [ (p.x, p.y - 1), (p.x, p.y + 1), (p.x - 1, p.y), (p.x + 1, p.y)]
    return [cave_map[y2][x2] for (x2, y2) in nsew
            if x_bound(x2) and y_bound(y2)]


def find_safest_path(cave_map, start, end):
    return find_paths(cave_map, start, end)


def find_paths(cave_map, here, end, path=None, i=0):
#    print("{}: {}: {}".format(i, here, path))
    paths = []

    if path == None:
        path = [here]
    else:
        if here in path:
            return []
        else:
            path.append(here)

    if here == end:
        paths.append(path)
    else:
        i += 1
        paths = [x for x in [find_paths(cave_map, p, end, path, i)
                             for p in adjacent(cave_map, here)]
                 if x != []]

    return paths


def point_xy(cave_map, x, y):
    return Point(x, y, cave_map[y][x])


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()

    # I initially called this variable 'map', which is allowed, but is
    # a terrible idea.  I didn't even notice the syntax highlight.
    cave_map = get_map(sys.stdin)

    start = cave_map[0][0]
    end = cave_map[-1][-1]
    path = find_safest_path(cave_map, start, end)
    pp.pprint(path)

