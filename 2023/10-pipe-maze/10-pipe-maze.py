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

if __name__ == "__main__":
    maze = get_maze(sys.stdin)
    print(find_start(maze))
