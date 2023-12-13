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

if __name__ == "__main__":
    patterns = get_ash_patterns(sys.stdin):
