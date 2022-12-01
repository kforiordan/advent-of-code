#!/usr/bin/env python3

# Counting groups of numbers.

# Well this is embarrassing:
#
#   First guess: 11668510
#   Second guess: 786159
#
# What am I doing wrong here?  Who knows.  Something stupid.  Deleted
# and rewrote and got correct answer.

import sys

if __name__ == "__main__":
    cals = -1
    max_cals = cals

    # I can write C in any language I choose.
    for line in sys.stdin:
        line = line.strip()
        if line == "":
            if cals != -1:
                if cals > max_cals:
                    max_cals = cals
                cals = -1
        else:
            if cals == -1:
                cals = int(line)
            else:
                cals += int(line)

    print(max_cals)
