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

my $n_fresh_ingredients = 0;
for my $ingredient (@ingredients) {
    for my $range (@ranges) {
	my $lower = $range->[0];
	my $upper = $range->[1];
	if ($ingredient >= $lower && $ingredient <= $upper) {
	    $n_fresh_ingredients++;
	    last;
	}
    }
}

print "$n_fresh_ingredients\n";
