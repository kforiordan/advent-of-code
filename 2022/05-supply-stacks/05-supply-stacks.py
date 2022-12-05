#!/usr/bin/env python3

import sys
import re

# Reads lists of chars from fh, returns list of tuples of tuples ...
def get_crate_stacks(fh):
    stacks = []

    for line in fh:
        line = line.rstrip('\n')
        #[Z] [M] [P]
        crates = get_crates(line)
        print(crates)
        exit(0)
        if line == "":
            break
        stacks.append(line)

    return stacks


def get_crates(line):
    crates = {}

    item_re = re.compile('\[([A-Z])\]')
    char_idx = 0
    stack_idx = 1
    while char_idx < len(line):
        line = line.rstrip(' \n')
        stack = line[char_idx:char_idx+3]
        m = item_re.search(stack)
        print(f'^{stack}$')
        if m:
            crates[stack_idx] = m.group(1)
        stack_idx += 1
        char_idx += 4	# 3 chars for crate, 1 for delimiting space.

    return crates


def get_moves(fh):
    moves = []

    for line in fh:
        line = line.rstrip('\n')
        moves.append(line)

    return moves


if __name__ == "__main__":

    stacks = get_crate_stacks(sys.stdin)
    moves = get_moves(sys.stdin)

    silver = "xzy"
    #gold = "123"
    print(f'Silver: {silver}')
    #print(f'Gold: {gold}')
