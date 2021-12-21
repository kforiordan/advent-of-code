#!/usr/bin/env perl

# https://adventofcode.com/2021/day/1#part2
#
# Similar to part 1, but with a sliding window comparison.

# This boils down to comparing the oldest element of the older window with the
# newest element of the newer window, but I used a queue anyway because why
# not.

use strict;
use warnings;

my $window_length = 3;

#my $in_fh = *DATA;
my $in_fh = *STDIN;

my $n = 0;
my @window;
my @diffs;
while (<$in_fh>) {
	chomp;
	last if (/^$/);	# This is just to handle my test data.

	push @window, $_;
	if ($n < $window_length) {
		$n++;
	}
	elsif ($n == $window_length) {
		my $left = shift @window;
		my $right = $window[-1];
		push @diffs, ($right - $left);
	}
}
print (scalar(grep {$_ > 0} @diffs)."\n");

__DATA__
199
200
208
210
200
207
240
269
260
263

A: 607 (N/A - no previous sum)
B: 618 (increased)
C: 618 (no change)
D: 617 (decreased)
E: 647 (increased)
F: 716 (increased)
G: 769 (increased)
H: 792 (increased)
