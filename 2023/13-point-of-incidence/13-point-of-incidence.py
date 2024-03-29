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


def row_eq(row_a, row_b, tolerance=0):
    smudge_count = 0
    for a,b in zip(row_a, row_b):
        if a == b:
            continue
        else:
            smudge_count += 1
            if smudge_count <= tolerance:
                continue
            return {'eq':False, 'smudge_count':smudge_count}

    return {'eq':True, 'smudge_count':smudge_count}


def is_mirrored(pattern, j, k, tolerance):
    t = tolerance
    while j >= 0 and k < len(pattern):
        result = row_eq(pattern[j], pattern[k], t)
        if result['eq'] == True:
            j -= 1
            k += 1
            t -= result['smudge_count']
        else:
            return result

    return {'eq':True, 'tolerance':t}


def horizontal_pattern_score(pattern, magic, tolerance):
    prev_row = None
    for i,row in enumerate(pattern):
        if prev_row != None:
            result = row_eq(prev_row, row, tolerance)
            if result['eq'] == True:
                result2 = is_mirrored(pattern, i-1, i, tolerance)
                if result2['eq'] == True and result2['tolerance'] == 0:
                    return {'score':(i * magic), 'smudge_count':result['smudge_count']}
        prev_row = row
    return None


def vertical_pattern_score(pattern, magic, tolerance):
    return horizontal_pattern_score(rotate90(pattern), magic, tolerance)


def silver(patterns, magic):
    magic = 100
    f = lambda x: x['score']
    return sum([f(pattern_score(p, magic)) for p in patterns])


def gold(patterns, magic):
    magic = 100
    smudge_tolerance = 1
    f = lambda x: x['score']
    g = lambda x: x['smudge_count']
    return sum([f(pattern_score(p, magic, smudge_tolerance)) for p in patterns])


if __name__ == "__main__":
    patterns = get_ash_patterns(sys.stdin)
    magic = 100
    print("Silver: {}".format(silver(patterns, magic)))
    print("Gold: {}".format(gold(patterns, magic)))
