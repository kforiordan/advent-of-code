# 2022, day 8: Treetop Tree House

## Problem Summary
Input is a dense grid of digits, each representing a tree of height given by
the digit.  A tree is visible if all of the other trees between it and an edge
of the grid are shorter than it (trees on each edge are also visible).

### Silver
Determine how many trees not visible?

### Gold
From each tree determine how many other trees can be seen in each direction,
multiply these numbers, report the largest such score.

## To Print Solutions
`cat prod-data.txt | python 08-treetop-tree-house.py`

Silver and gold solutions are both printed

## Note
For both solutions I checked all elements of the grid but, for different
reasons, there was no need to check the edge in ether case.  This is a simple
optimisation, but there are no points for runtime speed, so I'm not doing it.
