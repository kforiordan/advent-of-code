#!/usr/bin/env python3

from functools import reduce

import sys

# Reads lists of chars from fh, returns list of tuples, each tuple
# containing half of a list of chars.
def get_sack_groups(fh):
    groups = []

    elf_n = 1	 # Elves are 1-indexed.
    group = []
    for line in fh:
        line = line.rstrip("\n")
        if elf_n < 3:
            group.append(line)
            elf_n += 1
        elif elf_n == 3:
            group.append(line)
            groups.append(group)
            group = []
            elf_n = 1
        else:
            print("lol panic")
            exit(1)

    return groups


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


# Returns the item present in all sacks in a group
def in_all_sacks_in_group(sacks):

    # Doing this with reduce requires a base case containing all
    # possible members of the set.  It's feasible to generate that set
    # for this problem, but it's not a good general solution.
    common = list(set(sacks[0]) & (set(sacks[1]) & set(sacks[2])))
    if len(common) == 1:
        return common.pop()
    else:
        print("FUCKIT: {}".format(", ".join(common)))
        exit(1)


if __name__ == "__main__":
    groups = get_sack_groups(sys.stdin)

    priorities = map(lambda group: prio(in_all_sacks_in_group(group)), groups)
    gold = reduce(lambda x,y: x+y, priorities, 0)

    print(f'Gold: {gold}')
