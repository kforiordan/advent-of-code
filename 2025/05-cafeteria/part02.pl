#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;

my @ranges;
my @ingredients;

sub count_intervals
{
    my $ranges_ref = shift;
    my $total;

    for my $range (@$ranges_ref) {
	my $lower = $range->[0];
	my $upper = $range->[1];

	$total += ($upper - $lower) + 1;
    }

    return $total;
}


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

my @sorted_ranges = sort {$a->[0] <=> $b->[0] || $a->[1] <=> $b->[1]} @ranges;
#print Dumper(\@sorted_ranges);
my (@minimal_ranges, @complex_ranges);

my @diffs;

my $i = 0;
for my $range (@sorted_ranges) {
    my $lower = $range->[0];
    my $upper = $range->[1];
    
    if (exists($sorted_ranges[$i+1])) {
	my $next_lower = $sorted_ranges[$i+1]->[0];
	my $next_upper = $sorted_ranges[$i+1]->[1];
	if ($lower == $next_lower) {
	    push @$range, "Subset of next range";
	    # Do nothing with this.  It's included in the next one anyway.
	}
	else {
	    if ($upper >= $next_lower) {
		push @$range, "Simple merge with next";
		# Push this to the next range, deal with it there.
		# Strictly not necessary!  Doesn't affect the count.
		$sorted_ranges[$i+1]->[0] = $lower;
	    }
	    elsif ($upper < $next_lower) {
		push @$range, "Isolated";
		# Keep this.
		push @minimal_ranges, $range;
	    }
	}
    }
    else {
	push @minimal_ranges, $range;
    }

    $i++;
}

print Dumper(\@sorted_ranges);
print "-- \n";
print Dumper(\@minimal_ranges);
print "-- \n";
print count_intervals(\@minimal_ranges)."\n";
   
# print Dumper(\@minimal_ranges);
# print "COMPLEX:\n";
# print Dumper(\@complex_ranges);
__END__
# print everything, pipe to sort|uniq|wc -l , hurrah.  Well, no, it's way too slow.
for my $range (@ranges) {
    my $i = $lower;
    while ($i <= $upper) {
	print "$i\n";
	$i++;
    }
}
