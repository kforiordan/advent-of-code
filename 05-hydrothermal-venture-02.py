
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __hash__(self):
        return hash('{},{}'.format(self.x, self.y))

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and \
                self.x == other.x and \
                self.y == other.y)


def get_point_pairs(fh):
    point_pairs = []

    for line in fh:
        (p1,arrow,p2) = line.strip().split()
        (x1, y1) = map(int,p1.split(','))
        (x2, y2) = map(int,p2.split(','))
        point_pairs.append((Point(x1,y1), Point(x2,y2)))

    return point_pairs


def points_on_line(p1, p2):
    def flexrange(a, b):
        if b >= a:
            return range(a, b+1)
        else:
            return range(a, b-1, -1)

    points = []

    if p1.x == p2.x:
        points = [Point(p1.x, y) for y in range(min(p1.y,p2.y),(max(p1.y,p2.y) + 1))]
    elif p1.y == p2.y:
        points = [Point(x, p1.y) for x in range(min([p1.x,p2.x]),(max(p1.x,p2.x) + 1))]
    else:
        points = [Point(x, y) for x,y in zip(flexrange(p1.x, p2.x), flexrange(p1.y, p2.y))]

    return points


if __name__ == "__main__":
    point_pairs = []
    point_pairs = get_point_pairs(sys.stdin)

    point_counts = {}
    for (p1,p2) in point_pairs:
        for p in points_on_line(p1,p2):
            if p in point_counts:
                point_counts[p] = point_counts[p] + 1
            else:
                point_counts[p] = 1

    threshold = 2
    count = 0
    for p,c in point_counts.items():
        if c >= threshold:
            count += 1

    print(count)
