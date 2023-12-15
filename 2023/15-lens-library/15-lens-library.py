#!/usr/bin/env python3

import sys

def get_init_seq(fh):
    steps = []
    for line in fh:
        for step in line.rstrip().split(','):
            steps.append(step)
    return steps

def naive_hash(steps):
    hash = None
    return hash

if __name__ == "__main__":
    steps = get_init_seq(sys.stdin)

