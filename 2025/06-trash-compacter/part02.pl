#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;
use List::Util qw(reduce);

my @digit_grid;
my @ops_vector;

# Columns that contain an operator also are the beginning of a set of
# calculation.
sub find_starting_columns
{
    my ($ops_ref) = @_;
    my @starts;

    my $i = 0;
    while ($i < scalar(@$ops_ref)) {
	if ($ops_ref->[$i] =~ m/[\+\*]/) {
	    push @starts, $i;
	}
	$i++;
    }

    return @starts;
}

sub number_in_column
{
    my ($grid_ref, $col) = @_;

    my @digits;
    
    for my $row (@$grid_ref) {
	push @digits, $row->[$col];
    }

    return int(join('' => @digits));
}



while (my $line = <>) {
    chomp $line;
    if ($line =~ m/^\s*[\*\+]/) {
	@ops_vector = split('' => $line);
    }
    else {
	push @digit_grid, [ map {$_ ne ' ' ? int($_) : $_} (split('' => $line)) ];
    }
}

my @starts = find_starting_columns(\@ops_vector);

#print Dumper(\@digit_grid);
#print Dumper($digit_grid[-1]);
#print Dumper(@starts);

#print(number_in_column(\@digit_grid, $starts[1]));

my @results;
my $i = 0;
for my $start (@starts) {
    my $j = $start;
    my $k;
    if (exists($starts[$i+1])) {
	$k = $starts[$i+1] - 1;
    }
    else {
	$k = -1;
    }

    my @numbers;
    if ($k == -1) {
	$k = $j+3;	# I am sorry.  This is so stupid but I have other things to do.
    }
    while ($j < $k) {
	# This exists() check is stupid and is mostly because of the $j+3 thing above.
	if (exists($digit_grid[0][$j])) {
	    push @numbers, number_in_column(\@digit_grid, $j);
	}
	$j++;
    }
    
    my $result;
    if ($ops_vector[$start] eq '+') {
	$result = reduce {$a+$b} @numbers;
    }
    elsif ($ops_vector[$start] eq '*') {
	$result = reduce {$a*$b} @numbers;
    }
    else {
	print "oh dear\n";
    }
    push @results, $result;
    $i++;
}

print((reduce {$a+$b} @results)."\n");
