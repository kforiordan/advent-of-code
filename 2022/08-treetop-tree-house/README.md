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
