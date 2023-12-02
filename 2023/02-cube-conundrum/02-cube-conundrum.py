#!/usr/bin/env python3

import sys
import re

def parse_game(line):
    game_counts = {"red":-1, "green":-1, "blue":-1}

    game_id_re = re.compile('^Game ([0-9]+): ')
    game_id_text, sets_text = line.split(': ')

    game_id = game_id_text.split(' ')[1]

    sets = [gt.strip().split(', ') for gt in sets_text.split(';')]
    for s in sets:
        for colour_count in s:
            n,c = colour_count.split(' ')
            #game_counts[c].append(n)
            if int(n) > game_counts[c]:
                game_counts[c] = int(n)

    return {"id":game_id, "counts":game_counts}


def get_game_counts(fh):
    game_counts = []

    for line in sys.stdin:
        game_counts.append(parse_game(line.strip()))
    return game_counts


if __name__ == "__main__":

    limits = {"red":12, "green":13, "blue":14}

    game_counts = get_game_counts(sys.stdin)

    is_possible = lambda g: g["counts"]["red"] <= limits["red"] and g["counts"]["green"] <= limits["green"] and g["counts"]["blue"] <= limits["blue"]

    possible_games = filter(is_possible, game_counts)

    id_sum = sum([int(x["id"]) for x in possible_games])

    print(id_sum)
