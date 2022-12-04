# 2022, day 3: Rucksack Reorganization

## Problem Summary
Each input line is a string, with each char representing a rucksack item.

### Silver
Split each line in two equal halves, find the one item common to each half,
determine the value of that item (a-z: 1-26, A-Z: 27-52), sum these values.

### Gold
Treat each three lines of input (e.g. lines 1-3, 4-6, etc.) as part of one
group, find the item common to each group, determine value, sum.

## To Print Solutions
- Silver: `cat prod-data.txt | python3 03-rucksack-reorganization-01.py`
- Gold: `cat prod-data.txt | python3 03-rucksack-reorganization-02.py`
