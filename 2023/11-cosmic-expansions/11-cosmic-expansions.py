#!/usr/bin/env python

import sys
import re

def get_raw_universe(fh):
    return [list(row.strip()) for row in fh]


if __name__ == "__main__":
    print(get_raw_universe(sys.stdin))
