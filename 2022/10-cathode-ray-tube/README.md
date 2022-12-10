# 2022, day 10: Cathode Ray Tube

## Problem Summary
Input is a series of instructions for a two-instruction CPU (attached to a
cathode ray tube device) or something.

Each instruction either changes the value of a register, X, or does nothing;
both instruction types take some number of cycles to complete.  The signal
strength is the current cycle multiplied by the value of the X register.

### Silver
Report the sum of every 20th signal strength.

### Gold

## To Print Solution
`cat prod-data.txt | python 10-cathode-ray-tube.py`

Silver and gold solutions are both printed
