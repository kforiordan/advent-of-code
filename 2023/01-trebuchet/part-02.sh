#!/bin/bash

input_file="test-data.txt"
input_file="test-data-02.txt"
input_file="prod-data.txt"


# lol
cat "$input_file" \
	| perl -pe 's/^(.*?)([0-9]|one|two|three|four|five|six|seven|eight|nine).*/$2/' \
	| sed \
	-e 's/one/1/g' \
	-e 's/two/2/g' \
	-e 's/three/3/g' \
	-e 's/four/4/g' \
	-e 's/five/5/g' \
	-e 's/six/6/g' \
	-e 's/seven/7/g' \
	-e 's/eight/8/g' \
	-e 's/nine/9/g' \
	> firsts.txt

cat "$input_file" \
	| perl -pe 's/^(.*)([0-9]|one|two|three|four|five|six|seven|eight|nine).*/$2/' \
	| sed \
	-e 's/one/1/g' \
	-e 's/two/2/g' \
	-e 's/three/3/g' \
	-e 's/four/4/g' \
	-e 's/five/5/g' \
	-e 's/six/6/g' \
	-e 's/seven/7/g' \
	-e 's/eight/8/g' \
	-e 's/nine/9/g' \
	> lasts.txt

paste firsts.txt lasts.txt | tr -d '\t' \
	| perl -ne '$total += $_; END {print "$total\n"}'
