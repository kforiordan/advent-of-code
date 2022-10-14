
import pprint
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    # # Can't override __init__ with NamedTuple
    # def __init__(self, x, y):
    #     self.x = int(x)
    #     self.y = int(y)

    def __hash__(self):
        return hash('{},{}'.format(self.x, self.y))

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and \
                self.x == other.x and \
                self.y == other.y)



def is_straight_line(p1, p2):
    if p1.x == p2.x or p1.y == p2.y:
        return True

    return False

def get_point_pairs(fh):
    pp = pprint.PrettyPrinter(compact=True)
    point_pairs = []

    for line in fh:
        (p1,arrow,p2) = line.strip().split()
        (x1, y1) = map(int,p1.split(','))
        (x2, y2) = map(int,p2.split(','))
        point_pairs.append((Point(x1,y1), Point(x2,y2)))

    return point_pairs


def points_on_line(p1, p2):
    points = []

    if p1.x == p2.x:
        points = [Point(p1.x, y) for y in range(min(p1.y,p2.y),(max(p1.y,p2.y) + 1))]
    elif p1.y == p2.y:
        points = [Point(x, p1.y) for x in range(min([p1.x,p2.x]),(max(p1.x,p2.x) + 1))]

    return points


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)

    point_pairs = []
    point_pairs = get_point_pairs(sys.stdin)

    straight_lines = []
    straight_line_pairs = [(p1,p2) for (p1,p2) in point_pairs if is_straight_line(p1,p2)]

    point_counts = {}
    for (p1,p2) in straight_line_pairs:
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
