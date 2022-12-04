# 2022, day 2: Rock, Paper, Scissors

## Problem Summary
Each input line is a game of Rock, Paper, Scissors: your opponent's move
followed by yours.

### Silver
Determine the sum of scores for each game - points are awarded both for outcome
and for which response you play.

### Gold
As Silver, but treat the encoded response move as an encoded *result* instead,
and determine the response needed to achieve that result.

## To Print Solutions
- Silver: `cat prod-data.txt | python3 02-rock-paper-scissors-01.py`
- Gold: `cat prod-data.txt | python3 02-rock-paper-scissors-02.py`

## Note
Better solutions use modular arithmetic instead of a matrix of comparisons.
People are so clever.
