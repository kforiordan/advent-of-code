#!/usr/bin/env python3

import sys


def get_ash_patterns(fh):
    patterns = []
    this_pattern = []
    for row in fh:
        if len(row) <= 1:
            patterns.append(this_pattern)
            this_pattern = []
        else:
            this_pattern.append(list(row.strip()))
    patterns.append(this_pattern)

    return patterns


# https://stackoverflow.com/questions/52342209/matrix-transpose-without-numpy-error-list-index-out-of-range
#
# Another suggestion on that page, list(zip(*pattern)), returns a list
# of tuples.
#
def transpose(pattern):
    return list(map(list, zip(*pattern)))


# Building on the above transpose
def rotate90(pattern):
    return [list(reversed(row)) for row in transpose(pattern)]


# Best rotate -90 implementation evar.
def rotate270(pattern):
    return rotate90(rotate90(rotate90(pattern)))


def pattern_score(pattern, magic, tolerance=0):
    p = horizontal_pattern_score(pattern, magic, tolerance)
    if p == None:
        moar_magic = 1
        p = vertical_pattern_score(pattern, moar_magic, tolerance)
        if p == None:
            print("well this is not right")
            exit(0)
    return p


def elementwise_eq(row_a, row_b, tolerance=0):
    smudge_count = 0
    for a,b in zip(row_a, row_b):
        if a == b:
            continue
        else:
            if a == '#':
                smudge_count += 1
                if smudge_count <= tolerance:
                    continue
            return False
    return True


def horizontal_pattern_score(pattern, magic, tolerance):
    prev_row = None
    for i,row in enumerate(pattern):
        if prev_row != None:
            if elementwise_eq(prev_row, row, tolerance):
                j,k = i-1,i
                found_nonmatching = False
                while j >= 0 and k < len(pattern):
                    if elementwise_eq(pattern[j], pattern[k], tolerance):
                        j -= 1
                        k += 1
                    else:
                        found_nonmatching = True
                        break
                if found_nonmatching:
                    continue
                else:
                    return i * magic
        prev_row = row
    return None


def vertical_pattern_score(pattern, magic, tolerance):
    return horizontal_pattern_score(rotate90(pattern), magic, tolerance)


def silver(patterns, magic):
    magic = 100
    return sum([pattern_score(p, magic) for p in patterns])


def gold(patterns, magic):
    magic = 100
    smudge_tolerance = 1
    return sum([pattern_score(p, magic, smudge_tolerance) for p in patterns])


if __name__ == "__main__":
    patterns = get_ash_patterns(sys.stdin)
    magic = 100
    print("Silver: {}".format(silver(patterns, magic)))
    print("Gold: {}".format(gold(patterns, magic)))
