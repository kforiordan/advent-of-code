#!/bin/bash

input_file="test-data.txt"
input_file="test-data-02.txt"
#input_file="prod-data.txt"


# This doesn't work, it renders eightwothree as eigh2three instead of 8wo3
cat "$input_file" | sed \
	-e 's/one/1/g' \
	-e 's/two/2/g' \
	-e 's/three/3/g' \
	-e 's/four/4/g' \
	-e 's/five/5/g' \
	-e 's/six/6/g' \
	-e 's/seven/7/g' \
	-e 's/eight/8/g' \
	-e 's/nine/9/g' \
	> 'preprocessed-input.txt'
input_file='preprocessed-input.txt'
cat "$input_file"
cat "$input_file" | sed -e 's/^[^0-9]*\([0-9]\).*/\1/' > firsts.txt
cat "$input_file" | rev | sed -e 's/^[^0-9]*\([0-9]\).*/\1/' > lasts.txt
paste firsts.txt lasts.txt | tr -d '\t' \
	| perl -ne '$total += $_; END {print "$total\n"}'
