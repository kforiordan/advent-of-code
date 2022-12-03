#!/usr/bin/env python3


import sys

def get_sacks(fh):
    sacks = []

    # Splits a list into halves, returns a tuple.
    def halves(l):
        return (l[0:int(len(l)/2)-1], l[int(len(l)/2):])

    for line in fh:
        sacks.append(tuple(halves(list(line))))

    return sacks


def prio(item):

    # python can't seem to do this, extend() doesn't return anything.
    # Oh, I still hate this language.
    for (p,c) in zip(range(1,52+1),list(range(ord("a"),ord("z")+1)

)

if __name__ == "__main__":
    sacks = get_sacks(sys.stdin)

    for sack in sacks:
        left, right = (sack)
        for l in (set(left) & set(right)):
            print(f'{l}')

#    print(f'Silver: {tally}')
