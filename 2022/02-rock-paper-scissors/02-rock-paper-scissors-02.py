#!/usr/bin/env python3

# A, B, C: opponent's rock, paper, scissors
# X, Y, Z: my lose, draw, win

import sys

def get_rps_games(fh):
    games = []

    for line in fh:
        games.append(tuple(line.strip().split(' ')))

    return games


if __name__ == "__main__":
    games = get_rps_games(sys.stdin)
    worth = {"rock": 1, "paper": 2, "scissors": 3}
    result = {"win": 6, "draw": 3, "lose": 0}
    tally = 0

    for game in games:
        # match appears in python 3.10, apparently.
        # But match doesn't return a value anyway, oh man, how does
        # anyone actually like this language.
        match game:
            case ("A", "X"):
                tally += worth["scissors"] + result["lose"]
            case ("A", "Y"):
                tally += worth["rock"] + result["draw"]
            case ("A", "Z"):
                tally += worth["paper"] + result["win"]

            case ("B", "X"):
                tally += worth["rock"] + result["lose"]
            case ("B", "Y"):
                tally += worth["paper"] + result["draw"]
            case ("B", "Z"):
                tally += worth["scissors"] + result["win"]

            case ("C", "X"):
                tally += worth["paper"] + result["lose"]
            case ("C", "Y"):
                tally += worth["scissors"] + result["draw"]
            case ("C", "Z"):
                tally += worth["rock"] + result["win"]

    print(f'Gold: {tally}')
