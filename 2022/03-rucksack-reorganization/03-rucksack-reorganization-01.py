#!/usr/bin/env python3

from functools import reduce

import sys

# Reads lists of chars from fh, returns list of tuples, each tuple
# containing half of a list of chars.
def get_sacks(fh):
    sacks = []

    # Splits a list into halves, returns a tuple.
    def halves(l):
        l.pop() # chomp
        left = l[0:int(len(l)/2)]
        right = l[int(len(l)/2):len(l)]
        return (left, right)

    for line in fh:
        sacks.append(tuple(halves(list(line))))

    return sacks


# Returns the priority for a given rucksack item
def prio(item):
    base_a = ord("a")
    base_A = ord("A")

    if ord(item) >= base_a and ord(item) <= base_a + 26:
        return 1 + ord(item) - base_a
    elif ord(item) >= base_A and ord(item) <= base_A + 26:
        return 27 + ord(item) - base_A
    else:
        return -1000000000000066600000000000001 # Belphegor's number


# Returns the item present in both compartments of a given sack
def in_both_compartments(sack):
    (left, right) = sack
    common = list(set(left) & set(right))
    if len(common) == 1:
        return common.pop()
    else:
        print(", ".join(["".join(left), "".join(right)]))
        exit(1)


if __name__ == "__main__":
    sacks = get_sacks(sys.stdin)

    priorities = map(lambda sack: prio(in_both_compartments(sack)), sacks)
    silver = reduce(lambda x,y: x+y, priorities, 0)

    print(f'Silver: {silver}')
