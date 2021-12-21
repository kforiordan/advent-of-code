#!/usr/bin/env perl

# https://adventofcode.com/2021/day/2
#
# "... the submarine can take a series of commands like forward 1, down 2, or up 3 ... 
#    forward X increases the horizontal position by X units.
#    down X increases the depth by X units.
#    up X decreases the depth by X units.
#
# Calculate the horizontal position and depth you would have after following
# the planned course. What do you get if you multiply your final horizontal
# position by your final depth?"

use strict;
use warnings;

my ($horiz, $depth) = (0, 0);

while (<>) {
	chomp;
	my ($command, $arg);

	if (/^(forward|up|down)\s+([0-9]+)/) {
		($command, $arg) = ($1, $2);
	}

	if ($command eq q(forward)) { $horiz += $arg }
	elsif ($command eq q(up)) { $depth -= $arg }
	elsif ($command eq q(down)) { $depth += $arg }
}
my $position = $horiz * $depth;
print "Horiz: $horiz; Depth: $depth; Position: $position\n"
