#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;

my @ranges;
my @ingredients;

while (<>) {
    chomp;
    if ($_ eq "") {
	while (<>) {
	    chomp;
	    push @ingredients, $_;
	}
    }
    else {
	push @ranges, [ split('-' => $_) ];
    }
}

# print everything, pipe to sort|uniq|wc -l , hurrah.  Well, no, it's way too slow.
for my $range (@ranges) {
    my $lower = $range->[0];
    my $upper = $range->[1];
    my $i = $lower;
    while ($i <= $upper) {
	print "$i\n";
	$i++;
    }
}
