#!/usr/bin/env python3

import sys


def get_maze(fh):
    return [list(line.rstrip()) for line in fh]


if __name__ == "__main__":
    print(get_maze(sys.stdin))
