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


def jokerize(hand):
    new_hand = {}
    if 'J' in hand:
        n_j = hand['J']
        new_hand = {k:v for k,v in hand.items() if k != 'J'}
        default_card = 'A'
        if new_hand == {}:
            new_hand = {default_card:5}
        else:
            f = lambda k: new_hand[k]
            cards_by_frequency = list(reversed(sorted(new_hand.keys(), key=f)))
            most_common_card = cards_by_frequency[0]
            equally_common_cards = [card for card,n in new_hand.items() if n == new_hand[most_common_card]]

            card_rank_order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
            card_scores = {k:i+1 for i,k in enumerate(reversed(card_rank_order))}

            highest_valued = list(reversed(sorted(equally_common_cards, key=lambda c: card_scores[c])))[0]
#            print(equally_common_cards)
#            print(list(reversed(sorted(equally_common_cards, key=lambda c: card_scores[c]))))

            new_hand[highest_valued] += n_j
    else:
        new_hand = hand

#    print(new_hand)
    return new_hand


def score_hand(h, jokers_wild=None):
    score = None

    if jokers_wild:
        h['hand'] = jokerize(h['hand'])

    v = sorted(h['hand'].values())
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

    card_rank_order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
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

    f = lambda x: score_hand(x, True)
    ranked = sorted(rounds, key=f)
    total_score = 0
    for i,round in enumerate(ranked):
#        print("{} -> {}".format(round["orig"], round["hand"]))
        this_score = (i+1) * round["bid"]
        total_score += this_score
    print("Gold: {}".format(total_score))
