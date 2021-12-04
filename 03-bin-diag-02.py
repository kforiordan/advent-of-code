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

def filter_report(report, position, bias=1, flip_criterion=False):
    sub_report = []

    if len(report) <= 1:
        sub_report = report
    else:
        freq = count_freq(report)
        n = len(report)
        criteria = [round(((bias/2) + x)/n) for x in freq]
        criterion = criteria[position]
        if flip_criterion == True:
            criterion = abs(criterion - 1)

        sub_report = [x for x in report if x[position] == criterion]

        print(f'Criterion: {criterion}')

    return sub_report


def whittle_report(report, position=0, bias=1, flip_criterion=False):
    solution_set = []

    print(f'Position: {position};  Bias: {bias}')

    sub_report = filter_report(report, position, bias, flip_criterion)
    print("-- ")

    if len(sub_report) <= 1:
        solution_set = sub_report
    else:
        position = position + 1
        solution_set = whittle_report(sub_report, position, bias,
                                      flip_criterion)

    return solution_set


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    oxygen_generator_rating = 0
    co2_scrubber_rating = 0
    life_support_rating = 0

    report = get_report(sys.stdin)

    s = whittle_report(report, 0, 1)
    oxygen_generator_rating = (binlist2int(s[0]))

    s = whittle_report(report, 0, 1, True)
    co2_scrubber_rating = (binlist2int(s[0]))

    life_support_rating = oxygen_generator_rating * co2_scrubber_rating
    pp.pprint(oxygen_generator_rating)
    pp.pprint(co2_scrubber_rating)
    pp.pprint(life_support_rating)
