#!/usr/bin/env python3

import sys

def get_init_seq(fh):
    steps = []
    for line in fh:
        for step in line.rstrip().split(','):
            steps.append(step)
    return steps

def naive_hash(steps):
    hashed_steps = []
    for s in steps:
        v = 0
        for c in s:
            v += ord(c)
            v = v * 17
            v = v % 256
        hashed_steps.append(v)

    return hashed_steps

if __name__ == "__main__":
    steps = get_init_seq(sys.stdin)
    print("Silver: {}".format(sum(naive_hash(steps))))

