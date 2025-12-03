#!/usr/bin/env perl

use strict;
use warnings;
use List::Util qw(reduce);

my $verbose = 1;

sub is_invalid2
{
    my @digits = @_;
    
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

    return 1;
}


sub is_invalid6
{
    return ($_[0] == $_[2] && $_[2] == $_[4] &&
	    $_[1] == $_[3] && $_[3] == $_[5]);
}

sub is_invalid9
{
    return ($_[0] == $_[3] && $_[3] == $_[6] &&
	    $_[1] == $_[4] && $_[4] == $_[7] &&
	    $_[2] == $_[5] && $_[5] == $_[8]);
}

sub is_invalid10
{
    return ($_[0] == $_[2] && $_[2] == $_[4] && $_[4] == $_[6] && $_[6] == $_[8] &&
	    $_[1] == $_[3] && $_[3] == $_[5] && $_[5] == $_[7] && $_[7] == $_[9]);
}

sub all_same
{
    my $p = shift;

    for (@_) {
	return 0 if ($p != $_);
	$p = $_;
    }

    return 1;
}


sub is_invalid
{
    my $n = shift;

    my @digits = split(// => "$n");

    # 9,596,086,139;

    if ($n < 10) {
	return 0;
    }
    if (all_same(@digits)) {
	print("same $n\n") if ($verbose);
	return 1;
    }
    if (scalar(@digits) % 2 == 0) {
	if (is_invalid2(@digits)) {
	    print("2seq: $n\n") if ($verbose);
	    return 1;
	}
    }
    if (scalar(@digits) % 6 == 0) {
	if(is_invalid6(@digits)) {
	    print("3x2: $n\n") if ($verbose);
	    return 1;
	}
    }
    if (scalar(@digits) % 9 == 0) {
	if (is_invalid9(@digits)) {
	    print("3x3: $n\n") if ($verbose);
	    return 1;
	}
    }
    if (scalar(@digits) % 10 == 0) {
	if(is_invalid10(@digits)) {
	    print("5x2: $n\n") if ($verbose);
	    return 1;
	}
    }

    return 0;
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
