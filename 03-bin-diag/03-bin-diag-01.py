#!/usr/bin/env python3

# Binary operations, but with strings.

import sys

freq = []
agg = []

def binlist2int(l):
    mag = 1
    i = 0

    for x in reversed(l):
        i += x * mag
        mag = mag * 2

    return(i)

def binlistxor(l):
    return([1 if x == 0 else 0 for x in l])


if __name__ == "__main__":
    n = 0
    for line in sys.stdin:
        bits = list(map(int, list(line.strip())))
        if len(freq) == 0:
            freq = bits
        else:
            for i, b in enumerate(bits):
                freq[i] += int(b)
        n = n + 1

    agg = [round(x/n) for x in freq]

    gamma = binlist2int(agg)
    epsilon = binlist2int(binlistxor(agg))

    power_consumption = gamma * epsilon

    print(f'Gamma -> {gamma}; Epsilon -> {epsilon}')
    print(f'Power Consumption -> {power_consumption}')
