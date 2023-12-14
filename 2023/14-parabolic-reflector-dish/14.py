#!/usr/bin/env python3

import sys

def get_whatever(fh):
    return [list(row.rstrip()) for row in fh]

if __name__ == "__main__":
    whatever = get_whatever(sys.stdin))
