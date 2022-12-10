#!/usr/bin/env python3

import sys
from functools import reduce
from copy import deepcopy


# Borrowed from 2021's day 13 solution
if __name__ == "__main__":

    # "... consider the signal strength (the cycle number multiplied
    # by the value of the X register) during the 20th cycle and every
    # 40 cycles after that (that is, during the 20th, 60th, 100th,
    # 140th, 180th, and 220th cycles)."

    addx_cycles = 2
    noop_cycles = 1
    cycle = 0
    strength = 1
    strengths = []

    sample_count = 0

    for line in sys.stdin:
        line = line.rstrip('\n')
        cmd = line[0:4]
        if cmd == 'noop':
            cycle += noop_cycles
        elif cmd == 'addx':
            cycle += addx_cycles

        if int((cycle + 20) / 40) > sample_count:
            sample_cycle = (int((cycle + 20) / 40) * 40) - 20
            strengths.append(sample_cycle * strength)
            sample_count += 1

        if cmd == 'addx':
            arg = int(line[5:])
            strength += arg

    print("Silver: {}".format(sum(strengths)))
#    print("Gold: {}".format(len(ledger["gold"].keys())))
