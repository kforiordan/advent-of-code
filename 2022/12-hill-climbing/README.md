# 2022, day 12: Hill Climbing Algorithm

## Problem Summary
Input describes a grid. Movement is allowed horizontally and
vertically, but only if the square to which you are moving is not more
than 1 unit higher than your current square.

### Silver
Start at position S, get to position E with the minimum number of steps.

### Gold
What's the shortest path from any point at elevation 'a' to the end point 'E'?
I'm pretty sure this is can be rephrased as: starting at position E, find the
shortest path to the nearest point at elevation 'a'.  That's the problem I
considered anyway, and it gave the correct answer.

## To Print Solution
`cat prod-data.txt | python 12-hill-climbing.py`

Silver and gold solutions are both printed

# Note
Runtime greater than 30 secs is not great.
