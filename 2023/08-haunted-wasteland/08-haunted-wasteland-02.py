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
    node_re = re.compile('^([0-9A-Z]+) = \(([0-9A-Z]+), *([0-9A-Z]+)\)')
    for line in fh:
        m = node_re.match(line.rstrip())
        if m:
            nodes[m.group(1)] = [m.group(2), m.group(3)]

    return nodes

def get_path(nodes, instructions, start='AAA'):
    path = []
    curr_step = start

    keep_going = True
    while keep_going:
        for i in instructions:
            path.append(curr_step)
            if list(curr_step)[2] == 'Z':
                keep_going = False
                break
            if curr_step == start and len(path) > 1:
                print("oh no we've gotten stuck")
                print(path)
                print(len(path))
                keep_going = False
                break
            this_is_stupid = None
            if i == 'L':
                this_is_stupid = 0
            elif i == 'R':
                this_is_stupid = 1
            curr_step = nodes[curr_step][this_is_stupid]

    return path

def get_path_distances(nodes, instructions=None):
    path_distances = {}
    for n in nodes:
        path = get_path(nodes, instructions, n)
        path_distances[n] = len(path) - 1
    return path_distances

def get_paths(nodes, instructions):
    paths = None
    return paths

if __name__ == "__main__":
    instructions = get_instructions(sys.stdin)
    nodes = get_nodes(sys.stdin)
    path_distances = get_path_distances(nodes, instructions)
    print(path_distances)
    exit(0)
#    paths = get_paths(nodes, instructions)
    print("Silver: {}".format(len(path)-1))
