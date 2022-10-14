#!/usr/bin/env perl

# https://adventofcode.com/2021/day/2#part2
#
# In addition to horizontal position and depth, you'll also need to track a
# third value, aim, which also starts at 0. The commands also mean something
# entirely different than you first thought:
#
#    down X increases your aim by X units.
#    up X decreases your aim by X units.
#    forward X does two things:
#        It increases your horizontal position by X units.
#        It increases your depth by your aim multiplied by X."

use strict;
use warnings;

my ($aim, $horiz, $depth) = (0, 0, 0);

while (<>) {
	chomp;
	my ($command, $arg);

	if (/^(forward|up|down)\s+([0-9]+)/) {
		($command, $arg) = ($1, $2);
	}

	if ($command eq q(forward)) { $horiz += $arg; $depth += ($aim * $arg) }
	elsif ($command eq q(up)) { $aim -= $arg }
	elsif ($command eq q(down)) { $aim += $arg }
}
my $position = $horiz * $depth;
print "Horiz: $horiz; Depth: $depth; Position: $position\n"
