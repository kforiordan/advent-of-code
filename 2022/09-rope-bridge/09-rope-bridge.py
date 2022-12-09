#!/usr/bin/env python3

import sys
from functools import reduce
from copy import deepcopy

# Borrowed from 2021's day 13 solution
class Point:
    x: int
    y: int

    def __init__(self, x, y=None):
        self.x = int(x)
        self.y = int(y)

    # <2022 kor> This doesn't look right.  I wonder what I was doing?
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.x == other.x and self.y == other.y)

    def __hash__(self):
        return hash('{},{}'.format(self.x, self.y))

    def __str__(self):
        return("({},{})".format(self.x, self.y))

    def __repr__(self):
        return("Point({}, {})".format(self.x, self.y))

    def move(self, direction:str):
        if direction == 'U':
            self.y += 1
        elif direction == 'D':
            self.y -= 1
        elif direction == 'L':
            self.x -= 1
        elif direction == 'R':
            self.x += 1
        else:
            print(f'wtf is {direction}')

    def is_touching(self, other):
        return self == other or self.is_adjacent(other)

    # Python's type annotations are bullshit.
    #def adjacent(self, other:Point):
    def is_adjacent(self, other):
        xdist = abs(self.x - other.x)
        ydist = abs(self.y - other.y)
        if xdist + ydist == 1:
            # Horizontally or vertically adjacent
            return True
        elif xdist == 1 and ydist == 1:
            # Diagonally adjacent
            return True
        return False

    # Python's type annotations are bullshit.
    #def move_to(self, other:Point):
    def move_to(self, other):
        if self.y != other.y:
            if self.y < other.y:
                self.y += 1
            elif self.y > other.y:
                self.y -= 1
        if self.x != other.x:
            if self.x < other.x:
                self.x += 1
            elif self.x > other.x:
                self.x -= 1


def get_instructions(fh):
    massage = lambda x: tuple([x[0], int(x[1])])
    return [massage(line.rstrip('\n').split(' ')) for line in fh]


def record_point(ledger, point:Point):
    historical_point = deepcopy(point)
    if historical_point in ledger:
        ledger[historical_point] += 1
    else:
        ledger[historical_point] = 1


if __name__ == "__main__":
    instructions = get_instructions(sys.stdin)

    # These are given in the puzzle spec, not in the puzzle input.
    # Part 2 is similar to part 1, but the rope has ten knots in it
    # instead of two; each knot moves according to the same rules
    # though.
    #
    # Extending the solution to ten knots is not too tricky, then we
    # just have to record the points for knot 1 (silver tail) and knot
    # 9 (gold tail) separately.
    #
    gold_rope_len = 10
    rope = [Point(0,0) for i in range(0,gold_rope_len)]

    ledger = {"silver":{}, "gold":{}}
    record_point(ledger["silver"],rope[-1])
    record_point(ledger["gold"],rope[-1])

    for (direction, distance) in instructions:
        for i in range(0, distance):
            rope[0].move(direction)
            for k in range(1, gold_rope_len):
                if not rope[k].is_touching(rope[k-1]):
                    rope[k].move_to(rope[k-1])
                    if k == 1:
                        record_point(ledger["silver"], rope[k])
                    elif k == gold_rope_len - 1:
                        record_point(ledger["gold"], rope[k])

    print("Silver: {}".format(len(ledger["silver"].keys())))
    print("Gold: {}".format(len(ledger["gold"].keys())))
