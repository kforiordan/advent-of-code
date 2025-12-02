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

    while ($n != 0) {
	if ($d eq 'R') {
	    $pos++;
	}
	elsif ($d eq 'L') {
	    $pos--;
	}
	if ($pos == 100) {
	    $pos = 0;
	}
	elsif ($pos == -100) {
	    $pos = 0;
	}
	if ($pos == 0) {
	    $zeroes++;
	}
	$n--;
    }
    if ($pos < 0) {
	$pos += 100;
    }
}
print("$zeroes\n");
