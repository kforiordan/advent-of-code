# 2022, day 1: Calorie Counting

## Problem Summary
Input is groups of calorie counts, one amount per line, groups delimited by
blank lines.

### Silver
Determine the group with the highest sum of calories.

### Gold
As Silver, but sum of the three highest groups.

## To Print Solutions

- Python
  - Silver: `cat prod-data.txt | python3 01-calorie-counting-01.py`
  - Gold: `cat prod-data.txt | python3 01-calorie-counting-02.py`
- shell (sed, GNU dc)
  - Silver: `cat prod-data.txt | bash 01-calorie-counting-01.sh`
  - Gold: `cat prod-data.txt | bash 01-calorie-counting-02.sh`

## Note/Bug
The shell solution requires GNU dc.  dc, a reverse Polish notation calculator,
works by pushing numbers to a stack and having operators pop them off.  When
there's only one item on the stack and GNU dc uses a 2 operand operator, GNU dc
prints a warning but leaves the stack unchanged.  Macos's dc prints a similar
warning but removes the item from the stack and discards it.  I don't know
which behaviour is correct, but my script relies on GNU dc's forgiving nature.
