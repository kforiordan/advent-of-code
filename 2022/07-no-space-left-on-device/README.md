
# 2022, day 7: No Space Left on Device

## Problem Summary
Input is a series of cd & ls commands and their output (name, type, size).
These commands show all the files and directories in a filesystem.

### Silver
Determine total size of all directories which have size <100,000 .

### Gold
Determine the size of the smallest directory which, if deleted, would leave at
least 30,000,000 units of storage available.

## To Print Solutions
`cat prod-data.txt | python 07-no-space-left-on-device.py`

Silver and gold solutions are both printed

## Note
This is a pretty terrible script, and it's about four or so times longer than
some of the neater solutions I've seen.
