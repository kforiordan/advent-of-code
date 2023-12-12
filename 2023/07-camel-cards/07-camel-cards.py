#!/usr/bin/env python3

import sys
import re


def get_stuff(fh):
    rounds_or_something = []

    for line in fh:
        hand, bid = {}, None
        hand_str, bid_str = line.rstrip().split(' ')
        bid = int(bid_str)
        for card in hand_str:
            if card in hand:
                hand[card] += 1
            else:
                hand[card] = 1
        rounds_or_something.append({'hand':hand, 'bid':bid})

    return rounds_or_something


if __name__ == "__main__":
    rounds = get_stuff(sys.stdin)
    print(rounds)
