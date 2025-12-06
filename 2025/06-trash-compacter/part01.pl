#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;
use List::Util qw(reduce);

my @columns;

while (<>) {
    chomp;
    s/^\s*//;
    my $i = 0;
    for my $n (split(/\s+/ => $_)) {
	if (exists($columns[$i])) {
	    if ($n eq '*' || $n eq '+' ) {
		push @{$columns[$i]}, $n;
	    }
	    else {
		push @{$columns[$i]}, int($n);
	    }
	}
	else {
	    $columns[$i] = [ int($n) ];
	}
	$i++;
    }
}

my @subtotals;
for my $c (@columns) {
    my $r;
    if ($c->[-1] eq '+') {
	delete($c->[-1]);
	$r = reduce {$a+$b} @{$c};
    }
    elsif ($c->[-1] eq '*') {
	delete($c->[-1]);
	$r = reduce {$a*$b} @{$c};
    }
    else {
	print Dumper($c);
	die;
    }
    push @subtotals, $r;
}

print((reduce{$a+$b} @subtotals)."\n");
