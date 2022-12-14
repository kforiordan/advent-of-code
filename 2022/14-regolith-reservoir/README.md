# 2022, day 14: Regolith Reservoir

## Problem Summary
Input describes a series of lines barriers in a 2d vertical grid.
Sand falls in from the top, and we can model which way it falls; the
lines act as barriers.

### Silver
Report how many units of sand accumulate before excess overflows.

### Gold
Add another barrier - a floor with y equal to the largest y value of any
barrier point in the input data plus two.  Now run the simulation again
stopping when sand accumulates to such a volume that it reaches the sand source
point.  Again, report how many units of sand accumulate.

## To Print Solution
`cat prod-data.txt | python 14-regolith-reservoir.py`

Silver and gold solutions are both printed

