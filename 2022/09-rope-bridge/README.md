# 2022, day 9: Rope Bridge

## Problem Summary
Input is a series of instructions that move the head of a rope around a grid. 
As the head moves, the tail follows according to a few rules.

### Silver
Count the number of unique grid points the tail visits.

### Gold
Consider a longer rope - instead of just a head and tail, there are eight more
knots in between.  Each knot follows the same rules as for part 1, moving
relative to the knot preceding it.  Again, count the unique grid points the
tail visits.

## To Print Solution
- Silver: `cat prod-data.txt | python 09-rope-bridge-01.py`
- Gold: `cat prod-data.txt | python 09-rope-bridge-02.py`

Silver and gold solutions are both printed

