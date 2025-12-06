#!/usr/bin/env perl

use warnings;
use strict;
use Data::Dumper;
use List::Util qw(reduce);

sub joltage { return int(join('' => @_)); }

sub joltage_digits
{
    my ($n_significant, @digits) = @_;
	
    if ($n_significant == 0) {
	return ();
    }

    my $n_reserved = $n_significant - 1;
    
    # Separate the list of digits into the left pool, from which we
    # choose the leftmost highest digit, and the right pool, which
    # we'll select from on the next iteration.
    my @left = @digits[0 .. $#digits-$n_reserved];
    my @right = @digits[scalar(@digits)-$n_reserved .. $#digits];

    my ($h, $i, $j) = (-1, 0, -1);
    for my $x (@left) {
	if ($x > $h) {
	    $h = $x;
	    $j = $i;
	}
	$i++;
    }
    
    my @next_right;
    while ($j+1 < scalar(@left)) {
	push @next_right, $left[$j+1];
	$j++;
    }
    push @next_right, $_ for (@right);

    my @joltage_digits;
    push(@joltage_digits, $h, joltage_digits($n_significant-1, @next_right));
    
    return @joltage_digits;
}

my @joltage_digits;

my $magic = 12;
while (<>) {
    chomp;
    push @joltage_digits, [ joltage_digits($magic, map {int($_)} (split('' => $_))) ];
}

my @joltages = map {joltage(@$_)} @joltage_digits;
print((reduce {$a+$b} @joltages)."\n");
