#!/usr/bin/env perl

use warnings;
use strict;
use Data::Dumper;

my @grid;


sub read_puzzle_input
{
    my $fh = shift;
    my @grid;

    while (my $line = <$fh>) {
	chomp $line;
	push @grid, [ split('' => $line) ];
    }
    return @grid;
}


sub adjacent
{
    my ($max_y, $y, $max_x, $x, $looking_for) = @_;
    my ($min_y, $min_x) = (0, 0);
    
    my $inb = sub {
	my ($y,$x) = @_;
	return ($y >= $min_y && $y <= $max_y && $x >= $min_x && $x <= $max_x);
    };
    
    my $count = 0;

    for my $p ([$y-1, $x-1], [$y-1, $x], [$y-1, $x+1],
	       [$y, $x-1], [$y, $x+1],
	       [$y+1, $x-1], [$y+1, $x], [$y+1, $x+1])
    {
	$count++ if &$inb($p->[0], $p->[1]) && $grid[$p->[0]][$p->[1]] eq $looking_for;
    }

    return $count;
}


@grid = read_puzzle_input(\*STDIN);
my $grid_height = scalar(@grid);
my $grid_width  = scalar(@{$grid[0]});
my @open_cells;
my $magic = 4;

my $y = 0;
for my $row (@grid) {
    my $x = 0;
    for my $cell (@$row) {
	my $c = $cell eq '@' ? adjacent($grid_height-1, $y, $grid_width-1, $x, '@') : -1;
	#print("$y, $x -> $c (".$cell.")\n");
	if ($c != -1 && $c < $magic) {
	    push @open_cells, [ $y, $x ];
	}
	$x++;
    }
    $y++;
}
print scalar(@open_cells)."\n";
