# 2022, day 5: Supply Stacks

## Problem Summary
Input depicts crates stacked in columns, followed by a line numbering each
column, then an empty line, and then a series of instructions, one per line,
for moving crates between stacks.

### Silver
Determine which crate ends up on top of each column.

### Gold
Similar, but crate movement rules are different - for part 1, a move
instruction might say to move >1 crates, but only one crate at a time could be
moved; part 2 allows multiple crates to be moved at once.

## To Print Solutions
  - Silver: `cat prod-data.txt | python 05-supply-stacks-01.py`
  - Gold: `cat prod-data.txt | python 05-supply-stacks-02.py`
