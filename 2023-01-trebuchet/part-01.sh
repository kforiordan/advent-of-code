#!/bin/bash

input_file="test-data.txt"
input_file="prod-data.txt"

cat "$input_file" | sed -e 's/^[^0-9]*\([0-9]\).*/\1/' > firsts.txt
cat "$input_file" | rev | sed -e 's/^[^0-9]*\([0-9]\).*/\1/' > lasts.txt
paste firsts.txt lasts.txt | tr -d '\t' \
	| perl -ne '$total += $_; END {print "$total\n"}'
