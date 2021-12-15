import sys
import pprint


class Point:
    x: int
    y: int
    v: int

    def __init__(self, x, y, v=None):
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
    m = []
    for y,line in enumerate(fh):
        l = []
        for x,v in enumerate(list(line.strip())):
            l.append(Point(x,y,v))
        m.append(l)
    return(m)


def adjacent(cave_map, path, p):
    min_y = 0
    min_x = 0
    max_y = len(cave_map) - 1
    max_x = len(cave_map[0]) - 1
    y_bound = lambda p: p.y >= min_y and p.y <= max_y
    x_bound = lambda p: p.x >= min_x and p.x <= max_x

    return [Point(x2,y2,cave_map[y2][x2])
            for (x2,y2) in [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]
            if x_bound(x2) and y_bound(y2)]


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()

    # I initially called this variable 'map', which is allowed, but is
    # a terrible idea.  I didn't even notice the syntax highlight.

    cave_map = get_map(sys.stdin)
