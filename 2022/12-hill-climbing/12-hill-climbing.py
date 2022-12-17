#!/usr/bin/env python3

import sys

def get_hill_map(fh):
    hill_map = [list(map(ord,list(line.rstrip('\n')))) for line in fh]
    start = {}
    end = {}

    #"Your current position (S) has elevation a, and the location that
    #should get the best signal (E) has elevation z."
    for y in range(0,len(hill_map)):
        for x in range(0,len(hill_map[y])):
            if hill_map[y][x] == ord("S"):
                start = {"y":y, "x":x}
                hill_map[y][x] = ord('a')
            elif hill_map[y][x] == ord("E"):
                end = {"y":y, "x":x}
                hill_map[y][x] = ord('z')

    return (hill_map, start, end)


# I'm going to try to get comfortable with using global vars.
# args: p:{"x","y"}, label:({"x","y"}, dist)
def set_label(p, label):
    labels[p["y"]][p["x"]] = label

def get_label(p):
    return labels[p["y"]][p["x"]]

def adjacent(pos):
    min_y = min_x = 0
    max_y = len(hill_map)-1
    max_x = len(hill_map[0])-1  # Assuming square map.

    # "During each step, you can move exactly one square up, down, left,
    # or right ..."
    candidates = []
    if pos["y"]-1 >= min_y:
        candidates.append({"y":pos["y"]-1, "x":pos["x"]})
    if pos["x"]-1 >= min_x:
        candidates.append({"y":pos["y"], "x":pos["x"]-1})
    if pos["y"]+1 <= max_y:
        candidates.append({"y":pos["y"]+1, "x":pos["x"]})
    if pos["x"]+1 <= max_x:
        candidates.append({"y":pos["y"], "x":pos["x"]+1})

    # "... the elevation of the destination square can be at most
    # one higher than the elevation of your current square"
    return [p for p in candidates if
            hill_map[p["y"]][p["x"]] - hill_map[pos["y"]][pos["x"]] <= 1]


def uphill_adjacent(pos):
    min_y = min_x = 0
    max_y = len(hill_map)-1
    max_x = len(hill_map[0])-1  # Assuming square map.

    # "During each step, you can move exactly one square up, down, left,
    # or right ..."
    candidates = []
    if pos["y"]-1 >= min_y:
        candidates.append({"y":pos["y"]-1, "x":pos["x"]})
    if pos["x"]-1 >= min_x:
        candidates.append({"y":pos["y"], "x":pos["x"]-1})
    if pos["y"]+1 <= max_y:
        candidates.append({"y":pos["y"]+1, "x":pos["x"]})
    if pos["x"]+1 <= max_x:
        candidates.append({"y":pos["y"], "x":pos["x"]+1})

    # Inverse of this rule:
    #   "... the elevation of the destination square can be at most
    #    one higher than the elevation of your current square"
    return [p for p in candidates if
            hill_map[pos["y"]][pos["x"]] - hill_map[p["y"]][p["x"]] <= 1]


def unlabelled(vs):
    return [v for v in vs if labels[v["y"]][v["x"]] == None]


def labelled_vertices():
    l = []
    for y in range(0,len(hill_map)):
        for x in range(0,len(hill_map[y])):
            if labels[y][x] != None:
                l.append({"y":y, "x":x})
    return l


if __name__ == "__main__":
    hill_map, start, end = get_hill_map(sys.stdin)
    labels = [[None for x in range(0,len(hill_map[y]))]
              for y in range(0,len(hill_map))]

    pos = start


    # Dijkstra's algorithm, from Goodaire and Parmenter.  I
    # implemented this last year for day 15 of AoC, but it seems my
    # solution ran very slowly.  I'm trying again.

    # "To find the shortest path from vertex A to vertex E ...
    # Step 1.  Assign to A the label (-,0)"
    # Label assigned is a tuple of the preceding node and the distance from A.
    set_label(pos, (None,0))

    # "Step 2.  For each labeled vertex u(x,d) and for each unlabeled
    # vertex v adjacent to u, compute d+w(e) where e = uv"
    while get_label(end) == None:
        lowest = None
        for u in labelled_vertices():
            for v in unlabelled(adjacent(u)):
                if lowest == None or get_label(u)[1]+1 < lowest[2]:
                    lowest = (u, v, get_label(u)[1] + 1)
        set_label(lowest[1], (lowest[0], lowest[2]))

    # Ok, we've found the optimum path, now reconstruct it and count the steps.
    path = []
    pos = end
    while pos != start:
        path.append(pos)
        pos = get_label(pos)[0]

    print("Silver: {}".format(len(path)))


    labels = [[None for x in range(0,len(hill_map[y]))]
              for y in range(0,len(hill_map))]
    set_label(end, (None,0))

    # "Step 2.  For each labeled vertex u(x,d) and for each unlabeled
    # vertex v adjacent to u, compute d+w(e) where e = uv"
    pos = end
    while hill_map[pos["y"]][pos["x"]] != ord("a"):
        lowest = None
        for u in labelled_vertices():
            for v in unlabelled(uphill_adjacent(u)):
                if lowest == None or get_label(u)[1]+1 < lowest[2]:
                    lowest = (u, v, get_label(u)[1] + 1)
        set_label(lowest[1], (lowest[0], lowest[2]))
        pos = lowest[1]

    path = []
    while pos != end:
        path.append(pos)
        pos = get_label(pos)[0]

    print("Gold: {}".format(len(path)))

