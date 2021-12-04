#!/usr/bin/env python3

# Binary operations, but with strings.

import sys
import pprint

freq = []
agg = []

def binlist2int(l):
    mag = 1
    i = 0

    for x in reversed(l):
        i += x * mag
        mag = mag * 2

    return(i)

def binlistxor(l):
    return([1 if x == 0 else 0 for x in l])


def get_report(fh):
    report = []

    for line in fh:
        bits = list(map(int, list(line.strip())))
        report.append(bits)

    return report

def count_freq(report):
    freq = []

    for e in report:
        if len(freq) == 0:
            freq = [lol for lol in e]	# Inelegant
        else:
            for i, b in enumerate(e):
                freq[i] += int(b)

    return freq

def filter_report(report, position, bias=1):
    sub_report = []

    if len(report) <= 1:
        sub_report = report
    else:
        freq = count_freq(report)
        n = len(report)
        criteria = [round(((bias/2) + x)/n) for x in freq]
        pp = pprint.PrettyPrinter(indent=4)
        criterion = criteria[position]
        sub_report = [x for x in report if x[position] == criterion]
        # pp.pprint(report)
        # pp.pprint(position)
        # pp.pprint(criteria)
        # pp.pprint(criterion)
        # pp.pprint(sub_report)
        # print("-- ")

    return sub_report


def whittle_report(report, position, bias=1):
    solution_set = []

    sub_report = filter_report(report, position, bias)

    if len(sub_report) <= 1:
        solution_set = sub_report
    else:
        position = position + 1
        solution_set = whittle_report(sub_report, position, bias)

    return solution_set

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    oxygen_generator_rating = 0
    co2_scrubber_rating = 0
    life_support_rating = 0

    report = get_report(sys.stdin)
    #freq = count_freq(report)
    #sub_report = filter_report(report, 0)
    s = whittle_report(report, 0, 1)

    oxygen_generator_rating = (binlist2int(s[0]))
