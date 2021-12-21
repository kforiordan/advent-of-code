#!/usr/bin/env perl

# https://adventofcode.com/2021/day/1

# "... count the number of times a depth measurement increases from the
# previous measurement. ...  How many measurements are larger than the previous
# measurement?"

my ($prev,$curr) = (undef,undef);
my $n = 0;

while (<>) {
	chomp;
	$curr = $_;
	defined($prev) && $curr > $prev && $n++;
	$prev = $curr;
}

print $n."\n";

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
