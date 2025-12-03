#!/usr/bin/env perl

use strict;
use warnings;
use List::Util qw(reduce);

sub is_invalid
{
    my $n = shift;

    my @digits = split(// => "$n");

    if (scalar(@digits) % 2 == 0) {
	my ($a, $b, $c, $d) = (0, int($#digits/2), int($#digits/2)+1, $#digits);

	my ($i, $j) = ($a, $c);
	while ($i <= $b) {
	    if ($digits[$i] == $digits[$j]) {
		$i++;
		$j++;
	    }
	    else {
		return 0;
	    }
	}
    }
    else {
	return 0;
    }

    return 1;
}


sub invalids
{
    my ($low, $high) = @_;
    my @n;

    my $low_order = order($low);
    
    my $i = $low;
    while ($i <= $high) {
	push(@n, $i) if (is_invalid($i));
	$i++;
    }

    return @n;
}

sub order { my $n = shift; return int(log10($n)) }

# https://perldoc.perl.org/functions/log
sub log10 {
    my $n = shift;
    return log($n)/log(10);
}

my @invalids;
while (<>) {
    chomp;
    my @ranges = split(',' => $_);
    for my $range (@ranges) {
	my ($low,$high) = split('-' => $range);
	push @invalids, invalids($low, $high);
    }
}

print((reduce {$a+$b} @invalids)."\n");
