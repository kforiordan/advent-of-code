import sys
import pprint

class Point:
    x: int
    y: int

    def __init__(self, x, y=None):
        if isinstance(x,list) and len(x) == 2:
            y = x[1]
            x = x[0]

        self.x = int(x)
        self.y = int(y)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.x and self.y)

    def __hash__(self):
        return hash('{},{}'.format(self.x, self.y))

    def __str__(self):
        return("({},{})".format(self.x, self.y))

    def __repr__(self):
        return("Point({}, {})".format(self.x, self.y))


class Fold:
    axis: str
    coord: int

    def __init__(self, axis, coord=None):
        if isinstance(axis,list) and len(axis) == 2:
            coord = axis[1]
            axis = axis[0]

        self.axis = str(axis)
        self.coord = int(coord)

    def __str__(self):
        return("{}={}".format(self.axis, self.coord))

    def __repr__(self):
        return("Fold({}, {})".format(self.axis, self.coord))


def get_points(fh):
    points = []
    for line in fh:
        p = line.strip().split(',')
        if len(p) < 2:
            break
        points.append(Point(p))
    return points


def get_folds(fh):
    folds = []
    for line in fh:
        junk, junk, fold_line = line.strip().split()
        folds.append(Fold(fold_line.split('=')))
    return(folds)


def fold_point(fold, point):
    folded_point = point

    if fold.axis == 'y':
        if fold.coord < point.y:
            folded_point = Point(point.x,
                                 (point.y + (2 * (fold.coord - point.y))))
    elif fold.axis == 'x':
        if fold.coord < point.x:
            folded_point = Point((point.x + (2 * (fold.coord - point.x))),
                                 point.y)

    return folded_point


def foldem(folds, points):
    uniq_points = {p:True for p in points}

    for f in folds:
        tmp = {}
        for p in uniq_points:
            tmp[p] = fold_point(f,p)
        uniq_points = {v:None for v in tmp.values()}

    return list(uniq_points.keys())


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)
    points = get_points(sys.stdin)
    folds = get_folds(sys.stdin)

    dots = foldem([folds[0]], points)
    print("{} dots visible after one fold ({})".format(
        len(dots), str(folds[0])))
