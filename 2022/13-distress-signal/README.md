# 2022, day 13: Distress Signal

## Problem Summary
Input is pairs of packets, delimited by blank lines.  Packets look like lists,
with each element being either an int or another similar list.

### Silver
Determine the pairs that are correctly ordered, according to some
comparison rules: ints compare as normal; lists compare recursively; ints can
be compared to lists by converting them into single element lists.  Report the
sum of the indices of pairs which are correctly ordered

### Gold
Similar, but unpair the packets and sort the whole lot - along with two
divider keys, given in the spec.  Report the indices of the dividers after
sorting.

## To Print Solution
`cat prod-data.txt | python 13-distress-signal.py`

Silver and gold solutions are both printed

