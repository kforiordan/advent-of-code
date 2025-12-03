#!/usr/bin/env perl

use warnings;
use strict;
use List::Util qw(reduce);

sub joltage
{
    my ($tens, $units, @digits) = @_;
	
    my $i = 2;
    if (!exists($digits[0])) {
	return ($tens * 10) + $units;
    }
    foreach my $digit (@digits) {
	if (defined($digit)) {
	    if ($units > $tens) {
		$tens = $units;
		$units = $digit;
	    }
	    elsif ($digit > $units) {
		$units = $digit;
	    }
	}
    }

    return ($tens * 10) + $units;
}

my @joltages;

while (<>) {
    chomp;
    push @joltages, joltage(split('' => $_));
}

print((reduce {$a+$b} @joltages)."\n");
