#!/usr/bin/env python3

import sys
import re

def get_scratchcards(fh):
    cards = []

    card_re = re.compile('Card ([ 0-9]+): *([ 0-9]+)\|([ 0-9]+)$')
    for line in fh:
        card = {}
        line = line.strip()
        m = card_re.match(line)
        card["orig_line"] = line
        card["game_id"] = m.group(1)
        card["winning_numbers"] = sorted(list(map(int, filter(lambda s: s.isdigit(), m.group(2).split(' ')))))
        card["my_numbers"] = list(map(int, filter(lambda s: s.isdigit(), m.group(3).split(' '))))
        cards.append(card)

    return cards


def my_winners(winning_numbers, my_numbers):
    wow = []

    for m in my_numbers:
        for n in winning_numbers:
            if m == n:
                wow.append(m)
                break

    return wow


if __name__ == "__main__":
    scratchcards = get_scratchcards(sys.stdin)
    score = 0
    for s in scratchcards:
        w = my_winners(s["winning_numbers"], s["my_numbers"])
        s["my_winners"] = w
        n_winners = len(w)
        if n_winners > 0:
            score += pow(2, n_winners-1)
    print("Silver: {}".format(score))

    rec_wins = [None for _ in range(len(scratchcards))]
    for i in reversed(range(len(scratchcards))):
        s = scratchcards[i]
        rec_wins[i] = 1
        for j,_ in enumerate(s["my_winners"]):
            j += 1
            if i+j < len(scratchcards):
                rec_wins[i] += rec_wins[i+j]

    print("Gold: {}".format(sum(rec_wins)))
