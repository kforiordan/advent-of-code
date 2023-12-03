#!/usr/bin/env python3

import sys

def get_schematic(fh):
    return [list(line.strip()) for line in fh]

def discover_numbers_and_symbols(schematic):
    numbers = []
    symbols = []
    noop_char = '.'

    n = {}
    for y,row in enumerate(schematic):
        if "x" in n:
            numbers.append(n)
            n = {}
        for x, c in enumerate(row):
            if c.isdigit():
                if "x" in n:
                    n["digits"].append(int(c))
                else:
                    n["y"] = y
                    n["x"] = x
                    n["digits"] = [int(c)]
            else:
                if "x" in n:
                    numbers.append(n)
                    n = {}
                if c != noop_char:
                    symbols.append({"y":y, "x":x, "symbol":c})
    if "x" in n:
        numbers.append(n)
        n = {}

    return numbers, symbols


if __name__ == "__main__":
    schematic = get_schematic(sys.stdin)

    numbers, symbols = discover_numbers_and_symbols(schematic)
    print(numbers)
    print(symbols)


