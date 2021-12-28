import sys
import pprint


class Point():
    x: int
    y: int
    v: int
    # label: (Point, label)
    #
    # This doesn't work: Point hasn't been defined yet, bah.  Probably
    # not doing anything useful anyway.  They're not type annotations
    # or hints, idk, what even are they?  They're a poor form of
    # documentation too.

    def __init__(self, **kwargs):
        self.x, self.y, self.v, self.label = \
            None, None, None, None

        for k,v in kwargs.items():
            if k in self.__dict__:
                if k in ['x', 'y', 'v']:
                    setattr(self, k, int(v))
                else:
                    setattr(self, k, v)
            else:
                raise KeyError(k)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.x == other.x and self.y == other.y)

    def __hash__(self):
        return hash('{},{}->{}'.format(self.x, self.y, self.v))

    def __str__(self):
        s = ', '.join(["{}={}".format(k, v)
                       for k,v in self.__dict__.items()
                       if v != None])
        return("Point(" + s + ")")

    def __repr__(self):
        s = ', '.join(["{}={}".format(k, v)
                       for k,v in self.__dict__.items()
                       if v != None])
        return("Point(" + s + ")")

    # Can't call this label, because functions and variables share the
    # same namespace.
    def set_label(self, x, d):
        self.label = (x, d)

    def prev(self):
        if self.label == None:
            return None
        else:
            x, d = self.label
            return x

    def cost(self):
        if self.label == None:
            return self.v
            return None
        else:
            x, d = self.label
            return d

    def labelled(self):
        return(self.label != None)

    def unlabelled(self):
        return(self.label == None)


def extrapolate_right(row, n):
    #return [((x+i-1)%9)+1 for i in range(0,n) for x in l]
    # Makes sense to use a for loop because we're modifying data in place
    # Oh wait, we're not, hmm, I'll change to list comp later.
    new_row = []
    for i in range(0, n):
        for p in row:
            pi = Point(x=(p.x + (i * len(row))), y=p.y,
                       v=(((p.v + i - 1) % 9) + 1))
            new_row.append(pi)

    return(new_row)


def copy_row(row, fv=None, fy=None):
    if fv == None:
        fv = lambda a: a
    if fy == None:
        fy = lambda a: a

    return [Point(x=p.x, y=fy(p.y), v=fv(p.v)) for p in row]


def extrapolate_down(rows, n):

    new_rows = []
    for i in range(0, n):
        for row in rows:
            fy = lambda y: y + (i*len(rows))
            fv = lambda v: ((v + i - 1) % 9) + 1
            new_rows.append(copy_row(row, fv, fy))

    return new_rows


def extrapolate(cave_map, n=5):
    extrapolated_map = []

    for row in cave_map:
        new_row = extrapolate_right(row, 5)
        extrapolated_map.append(new_row)

    extrapolated_map = extrapolate_down(extrapolated_map, 5)
    return(extrapolated_map)


def get_map(fh):
    ys = []
    for y,line in enumerate(fh):
        xs = []
        for x,v in enumerate(list(line.strip())):
            xs.append(Point(x=x,y=y,v=v))
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


def dijkstra(cave_map, start, end):

    # Quotations here are transcribed from Goodaire and Parmenter

    # "Step 1. Assign to A the label (-, 0)"
    start.set_label(None, 0)

    # "Step 2. Until E is labelled or no further labels can be
    # assigned, do the following."

    curr = start
    labelled_vertices = [start]
    exhausted_adjacent_vertices = []
    while True:

        unlabelled_adjacent_vertices = []
        for v in labelled_vertices:
            a = adjacent(cave_map, v)
            if len(a) > 0:
                for x in a:
                    if x.unlabelled():
                        unlabelled_adjacent_vertices.append((v, x))
            else:
                exhausted_adjacent_vertices.append(v)

        if len(unlabelled_adjacent_vertices) == 0:
#            pp.print(labelled_vertices)
            exit(0)

        (v, x) = min(unlabelled_adjacent_vertices,
                     key=lambda uav: uav[0].cost() + uav[1].cost())

        x.set_label(v, v.cost() + x.cost())

        if x == end:
            # pp.pprint(v)
            # pp.pprint(x)
            break

        labelled_vertices.append(x)

    return x


def point_xy(cave_map, x, y):
    return Point(x, y, cave_map[y][x])


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()

    cave_map = extrapolate(get_map(sys.stdin), 5)

    start = cave_map[0][0]
    end = cave_map[-1][-1]
    path = dijkstra(cave_map, start, end)

    print(path.cost())

