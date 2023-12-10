#!/usr/bin/env python3

import sys
import re

def get_oasis_reports(fh):
    return [list(map(int, line.rstrip().split(' '))) for line in fh]


def get_differences(report):
    prev = None
    diffs = []
    for curr in report:
        if prev != None:
            diffs.append(curr - prev)
        prev = curr
    return diffs


def all_zeroes(diffs):
    for d in diffs:
        if d != 0:
            return False
    return True


def predict_next(report):
    if all_zeroes(report):
        return 0
    else:
        return report[-1] + predict_next(get_differences(report))


if __name__ == "__main__":

    reports = get_oasis_reports(sys.stdin)
    print("Silver: {}".format(sum(map(predict_next, reports))))

    # hahaha this is stupid
    stupid = list(map(list,map(reversed, reports)))
    print("Gold: {}".format(sum(map(predict_next, stupid))))

    # Look, I get it, this was meant to be about recursion, but the
    # above was funnier and quicker and oh man I am so far behind at
    # the moment.
