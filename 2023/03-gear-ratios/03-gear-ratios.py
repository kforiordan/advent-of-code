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

    for n in numbers:
        i = 0
        number = 0
        for d in reversed(n["digits"]):
            number += d * pow(10,i)
            i += 1
        n["value"] = number

    return numbers, symbols


def is_symbol(schematic, y, x):
    # This is a weak definition of a symbol.
    return not schematic[y][x].isdigit() and not schematic[y][x] == '.'

def in_bounds(schematic, y, x):
    return y >= 0 and y < len(schematic) and x >= 0 and x < len(schematic[0])

def symbol_adjacent(schematic,  y, x):
    f = lambda y, x: in_bounds(schematic, y, x) and is_symbol(schematic, y, x)

    return f(y-1, x-1) or f(y-1, x) or f(y-1, x+1)


def symbol_adjacent_numbers(numbers, symbols):
    for n in numbers:
        print(n)


    return []


if __name__ == "__main__":
    schematic = get_schematic(sys.stdin)

    numbers, symbols = discover_numbers_and_symbols(schematic)

    good_numbers = symbol_adjacent_numbers(numbers, symbols)

    print(numbers)
