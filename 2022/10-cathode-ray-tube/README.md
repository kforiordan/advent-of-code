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
Every cycle, we draw a pixel.  The pixel is lit if a sprite overlaps the
current pixel position, or unlit if not.  The sprite's position is specified by
register X - plus the positions either side of it.  With this in mind, the
printed output is a rendering of eight ascii chars.

## To Print Solution
`cat prod-data.txt | python 10-cathode-ray-tube.py`

Silver and gold solutions are both printed

## Note
My summary of the gold spec is unclear, so you'd have to read the spec to get a
proper understanding of the problem, but the spec itself was difficult to
understand.
