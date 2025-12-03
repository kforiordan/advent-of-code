#!/usr/bin/env perl

use warnings;
use strict;
use List::Util qw(reduce);

sub joltage
{
    my ($tens, $units, @digits) = @_;
	
    foreach my $digit (@digits) {
	if ($units > $tens) {
	    $tens = $units;
	    $units = $digit;
	}
	elsif ($digit > $units) {
	    $units = $digit;
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
