#!/usr/bin/env python3

# Counting scores for successive games of rock paper scissors.  Turns
# out the smart solution - which I didn't do - is to encode as ints
# and do mod 3 comparison.

import sys

def get_rps_games(fh):
    games = []

    for line in fh:
        games.append(tuple(line.strip().split(' ')))

    return games


if __name__ == "__main__":
    games = get_rps_games(sys.stdin)
    worth = {"X": 1, "Y": 2, "Z": 3}
    result = {"win": 6, "draw": 3, "lose": 0}
    tally = 0

    for game in games:
        # match appears in python 3.10, apparently.
        # But match doesn't return a value anyway, oh man, how does
        # anyone actually like this language.
        match game:
            case ("A", "X"):
                tally += worth["X"] + result["draw"]
            case ("A", "Y"):
                tally += worth["Y"] + result["win"]
            case ("A", "Z"):
                tally += worth["Z"] + result["lose"]

            case ("B", "X"):
                tally += worth["X"] + result["lose"]
            case ("B", "Y"):
                tally += worth["Y"] + result["draw"]
            case ("B", "Z"):
                tally += worth["Z"] + result["win"]

            case ("C", "X"):
                tally += worth["X"] + result["win"]
            case ("C", "Y"):
                tally += worth["Y"] + result["lose"]
            case ("C", "Z"):
                tally += worth["Z"] + result["draw"]

    print(f'Silver: {tally}')
