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
        rounds_or_something.append({'hand':hand, 'bid':bid, 'orig':hand_str})

    return rounds_or_something


def score_hand(h):
    n = len(h['hand'].keys())
    v = sorted(h['hand'].values())
    score = None
    card_rank_order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    if v == [5]:
        # five of a kind
        score = 300000000
    elif v == [1,4]:
        # four of a kind
        score = 290000000
    elif v == [2,3]:
        # full house
        score = 280000000
    elif v == [1,1,3]:
        # three of a kind
        score = 270000000
    elif v == [1,2,2]:
        # two pair
        score = 260000000
    elif v == [1,1,1,2]:
        # one pair
        score = 250000000
    else:
        # high card
        score = 240000000

    card_scores = {k:i+1 for i,k in enumerate(reversed(card_rank_order))}
    for i,card in enumerate(reversed(h['orig'])):
        score += pow(len(card_rank_order), i+1) * card_scores[card]

    return score

if __name__ == "__main__":
    rounds = get_stuff(sys.stdin)

    ranked = sorted(rounds, key=score_hand)
    total_score = 0
    for i,round in enumerate(ranked):
        this_score = (i+1) * round["bid"]
        total_score += this_score

    print("Silver: {}".format(total_score))
