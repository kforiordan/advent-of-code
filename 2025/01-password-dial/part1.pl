#!/usr/bin/env perl

use strict;
use warnings;

my $initial_position = 50;
my $pos = $initial_position;
my $zeroes = 0;

while (<>) {
    chomp;
    my ($d,@n) = split('');
    my $n = int(join("" => @n));

    if ($d eq 'L') {
	$pos -= $n;
    }
    elsif ($d eq 'R') {
	$pos += $n;
    }
    $pos = $pos % 100;
    $zeroes++ if ($pos == 0);
}

print ("$zeroes\n");
