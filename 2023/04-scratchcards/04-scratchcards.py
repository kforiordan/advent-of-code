#!/usr/bin/env python3

import sys
import re

def get_scratchcards(fh):
    cards = []

    card_re = re.compile('Card ([ 0-9]+): *([ 0-9]+)\|([ 0-9]+)$')
    for line in fh:
        line = line.strip()
        m = card_re.match(line)
        id = m.group(1)
        winning_numbers = sorted(list(map(int, filter(lambda s: s.isdigit(), m.group(2).split(' ')))))
        my_numbers = list(map(int, filter(lambda s: s.isdigit(), m.group(3).split(' '))))
        print(id)
        print(winning_numbers)
        print(my_numbers)
        print("-- ")

    return cards


if __name__ == "__main__":
    scratchcards = get_scratchcards(sys.stdin)
