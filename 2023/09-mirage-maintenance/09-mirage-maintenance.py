#!/usr/bin/env python3

import sys
import re

def get_oasis_reports(fh):
    return [list(map(int, line.rstrip().split(' '))) for line in fh]


if __name__ == "__main__":
    print(get_oasis_reports(sys.stdin))
