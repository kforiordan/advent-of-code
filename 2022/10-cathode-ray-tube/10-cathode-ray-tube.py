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
    register_x = 1

    strengths = []
    sample_count = 0

    pixels = []
    sprite_position = 1 # middle of sprite, actually 0 & 2 also.

    for line in sys.stdin:
        line = line.rstrip('\n')
        cmd = line[0:4]
        cmd_arg = None
        if cmd == 'noop':
            op_cycles = noop_cycles
        elif cmd == 'addx':
            op_cycles = addx_cycles
            cmd_arg = int(line[5:])

        # "... the CRT draws a single pixel during each cycle ...
        lit_pixel = "#"
        dark_pixel = " "  # In the spec this is '.', but space is more readable.
        for i in range(0, op_cycles):
            if abs(cycle % 40 - register_x) <= 1:
                pixels.append(lit_pixel)
            else:
                pixels.append(dark_pixel)
            cycle += 1
            if int((cycle + 20) / 40) > sample_count:
                sample_cycle = (int((cycle + 20) / 40) * 40) - 20
                strengths.append(sample_cycle * register_x)
                sample_count += 1
            if cycle % 40 == 0:
                pixels.append('\n')

        if cmd == 'addx':
            register_x += cmd_arg

    print("Silver: {}".format(sum(strengths)))
    print("Gold:")
    print("".join(pixels))
