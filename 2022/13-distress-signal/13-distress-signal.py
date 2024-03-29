#!/usr/bin/env python3

import sys
import re
from functools import reduce, cmp_to_key

# Returns list of two strings, each of which is a signal.
def get_pairs(fh):
    pairs = []

    pair = []
    for line in fh:
        line = line.rstrip('\n')
        if line == "":
            if len(pair) == 2:
                pairs.append(pair)
                pair = []
        else:
            pair.append(values(line))
    if pair != []:
        pairs.append(pair)

    return pairs


# "Each list starts with [, ends with ], and contains zero or more
# comma-separated values (either integers or other lists)."
#
# Given a string enclosed by brackets, returns a list
def values(s):
    # TYPE CHECKING.  YES, I WILL BE WRITING A PEP PROPOSAL.
    if s[0] != "[":
        print("missing open bracket: '{}'".format(s))
        exit(1)
    if s[-1] != "]":
        print("missing closing bracket: '{}'".format(s))
        exit(1)
    s = s[1:]
    s = s[:-1]

    number_re = re.compile('([0-9]+)')
    i = 0
    v = []
    while i < len(s):
        m = number_re.match(s[i:])
        if m:
            v.append(int(m.group(1)))
            i += len(m.group(1))
        elif s[i] == "[":
            depth = 1
            sv = []
            sv.append(s[i])
            while depth > 0:
                i += 1
                if s[i] == "[":
                    depth += 1
                elif s[i] == "]":
                    depth -= 1
                sv.append(s[i])
            i += 1
            v.append(values("".join(sv)))
        elif s[i] == ",":
            i += 1
        else:
            print("wtf: {} at {} after {} in {}".format(s[i], i, v, s))
            exit(0)

    return v


# Given two lists of signal components, returns -1 if left < right; else 1 ... or 0
def compare(left, right):
    if isinstance(left, list) and isinstance(right, list):
        if left == []:
            if right == []:
                return 0
            else:
                return -1
        elif right == []:
            return 1
        else:
            # Two non-empty lists: 
            corollary = compare(left[0], right[0])
            if corollary == 0:
                return compare(left[1:], right[1:])
            else:
                return corollary
    elif isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        return 0
    elif isinstance(left, int):
        left = [left]
        return compare(left, right)
    elif isinstance(right, int):
        right = [right]
        return compare(left, right)
    else:
        print("HOW DID WE GET HERE ARGH")
        print("L-R: '{}' -- '{}'".format(left, right))

    print("OK THERE IS NO WAY WE COULD HAVE GOTTEN HERE WHAT HAPPENED")
    print("Types (l, r): ({}, {})".format(type(left), type(right)))


if __name__ == "__main__":
    pairs = get_pairs(sys.stdin)
    ordered_pair_indices = [(i+1) for i,pair in enumerate(pairs) if compare(pair[0], pair[1]) == -1]
    print("Silver: {}".format(sum(ordered_pair_indices)))

    packets = []
    for p in pairs:
        packets.append(p[0])
        packets.append(p[1])
    # Now add the magic divider packets:
    packets.append([[2]])
    packets.append([[6]])

    sorted_packets = sorted(packets, key=cmp_to_key(compare))
    divider_packet_indices = [(i+1) for i,p in enumerate(sorted_packets) if p == [[2]] or p == [[6]]]
    print("Gold: {}".format(reduce(lambda a,b: a*b, divider_packet_indices, 1)))
