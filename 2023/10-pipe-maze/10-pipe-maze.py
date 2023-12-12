#!/usr/bin/env python3

import sys


def get_maze(fh):
    return [list(line.rstrip()) for line in fh]


def find_start(maze, start='S'):
    for y,row in enumerate(maze):
        for x,cell in enumerate(row):
            if cell == start:
                return (y,x)
    return (-1,-1)


def in_bounds(maze, y, x):
    if y >= 0 and y < len(maze) and x >= 0 and x < len(maze[0]):
        return True
    return False


# returns list of tuples of connected tunnel segments.
def find_connected(maze, y, x):
    c = maze[y][x]
    connected = []
    allowed_connections = {
        'S': { (-1,  0): '-|7FJL',
               ( 0, -1): '-|7FJL',
               ( 0,  1): '-|7FJL',
               ( 1,  0): '-|7FJL' },
        '|': { (-1,  0): '7|FS',
               ( 1,  0): 'J|LS' },
        '-': { ( 0, -1): 'L-FS',
               ( 0,  1): 'J-7S' },
        '7': { ( 0, -1): 'L-FS',
               ( 1,  0): 'L|JS', },
        'F': { ( 0,  1): 'J-7S',
               ( 1,  0): 'L|JS' },
        'J': { (-1,  0): '7|FS',
               ( 0, -1): 'L-FS' },
        'L': { (-1,  0): '7|FS',
               ( 0,  1): 'J-7S' },
    }
    for (oy,ox),v in allowed_connections[c].items():
        y2, x2 = y+oy, x+ox
        if in_bounds(maze, y2, x2) and maze[y2][x2] in v:
            connected.append((y2, x2))

    return connected


def find_path(maze, start):
    seen = {}
    path = []

    prev_step, curr_step, next_step = None, start, None
    while True:
        if curr_step in seen:
            seen[curr_step] += 1
            break
        else:
            seen[curr_step] = 1
        options = find_connected(maze, *curr_step)
        if prev_step == None:
            next_step = options[0]
        else:
            next_step = list(filter(lambda x: x != prev_step, options))[0]
        prev_step = curr_step
        path.append(next_step)
        curr_step = next_step

    return path

if __name__ == "__main__":
    maze = get_maze(sys.stdin)

    start = find_start(maze)
    looped_path = find_path(maze, start)

    print("Silver: {}".format(int(len(looped_path)/2)))
