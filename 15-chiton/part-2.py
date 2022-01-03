import sys
import pprint

# numpy has a better infinity than this
infinity_lol=98765432

class Point():
    x: int
    y: int
    v: int
    tmp_label: int
    label: int

    def __init__(self, **kwargs):
        self.x, self.y, self.v, self.label = \
            None, None, None, None
        self.tmp_label = infinity_lol

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

    def set_label(self, v):
        self.label = v

    def set_tmp_label(self, v):
        self.tmp_label = v

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
            xs.append(Point(x=x,y=y,v=v,tmp_label=infinity_lol))
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


def dijkstra_improved(cave_map, start, end):

    # Quotations here are transcribed from Goodaire and Parmenter

    # 1. "Set v_1=A and assign to this vertex the permanent label 0."
    start.set_label(0)
    most_recently_labelled = start

    #    "Assign every other vertex a temporary label of ∞"
    #
    #    This is done by default at Point() instantiation time.

    # 2. "Until E has been assigned a permanent label or no temporary
    #    labels are changed in (a) or (b), do the following:"
    #
    while end.unlabelled():

        # (a) "Take the vertex v_i that most recently acquired a
        # permanent label ... For each vertex v that is adjacent to
        # v_i and has not yet received a permanent label, if
        # d+w(v_i→v) < t, the current temporary label of v, change the
        # temporary label of v to d + w(v_i→v)"
        for vertex in adjacent(cave_map, most_recently_labelled):
            if vertex.unlabelled():
                cost = most_recently_labelled.label + vertex.v
                if cost < vertex.tmp_label:
                    vertex.set_tmp_label(cost)

        # (b) "Take a vertex v that has a temporary label smallest
        # among all temporary labels in the graph.  Set v_i+1 = v and
        # make its temporary label permanent."
        candidates = [vertex for row in cave_map for vertex in row \
                      if vertex.unlabelled()]
        nearest = min(candidates, key=lambda x: x.tmp_label)
        nearest.set_label(nearest.tmp_label)
        most_recently_labelled = nearest

    return end.label


def point_xy(cave_map, x, y):
    return Point(x, y, cave_map[y][x])


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()

    cave_map = extrapolate(get_map(sys.stdin), 5)

    start = cave_map[0][0]
    end = cave_map[-1][-1]
    path_cost = dijkstra_improved(cave_map, start, end)

    print(path_cost)
