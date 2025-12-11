#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;

my (@beams, @splitters);
my ($start_char, $beam_char, $splitter_char) = qw(S | ^);

my $y = 0;
while (<>) {
    chomp;
    my $x = 0;
    for my $cell (split('' => $_)) {
	if ($cell eq $start_char) {
	    push @beams, [ $y, $x ];
	}
	elsif ($cell eq $splitter_char) {
	    push @splitters, [ $y, $x ];
	}
	$x++;
    }
    $y++;
}

print Dumper(\@beams);
print Dumper(\@splitters);

