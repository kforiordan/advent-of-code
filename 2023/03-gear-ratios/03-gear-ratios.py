#!/usr/bin/env python3

import sys

def get_schematic(fh):
    return [list(line.strip()) for line in fh]

if __name__ == "__main__":
    schematic = get_schematic(sys.stdin)
