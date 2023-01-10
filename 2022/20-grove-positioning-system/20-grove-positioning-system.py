#!/usr/bin/env python3

import sys

from node import Node
from circularlist import CircularList

#!/usr/bin/env python3

def get_numbers(fh):
    return [int(n.rstrip('\n')) for n in fh]


if __name__ == "__main__":
    numbers = get_numbers(sys.stdin)

    clist = CircularList(numbers)

    print("Before: {}".format(clist.get_vals()))
    clist.mix()
    print("After: {}".format(clist.get_vals()))

