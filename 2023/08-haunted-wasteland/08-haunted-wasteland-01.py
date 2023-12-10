#!/usr/bin/env python3

import sys
import re


def get_instructions(fh):
    instructions = []
    for line in fh:
        instructions = list(line.strip())
        break
    return instructions


def get_nodes(fh):
    nodes = {}
    node_re = re.compile('^([A-Z]+) = \(([A-Z]+), *([A-Z]+)\)')
    for line in fh:
        m = node_re.match(line.rstrip())
        if m:
            nodes[m.group(1)] = [m.group(2), m.group(3)]

    return nodes

def get_path(nodes, instructions):
    path = []
    start, end = 'AAA', 'ZZZ'
    curr_step = start

    keep_going = True
    while keep_going:
        for i in instructions:
            path.append(curr_step)
            if curr_step == end:
                keep_going = False
                break
            this_is_stupid = None
            if i == 'L':
                this_is_stupid = 0
            elif i == 'R':
                this_is_stupid = 1
            curr_step = nodes[curr_step][this_is_stupid]

    return path

if __name__ == "__main__":
    instructions = get_instructions(sys.stdin)
    nodes = get_nodes(sys.stdin)
    path = get_path(nodes, instructions)
    print("Silver: {}".format(len(path)-1))
