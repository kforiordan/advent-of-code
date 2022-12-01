#!/bin/bash

# Requires GNU dc.  On macos, + with only one number on the stack pops and
# discards that number, and it's lost.  GNU dc leaves the stack unchanged.  I
# don't know which behaviour is correct, but I'm relying on GNU's.

sed 's/$/ +/;s/^[ +]*$/pc/' | dc 2>/dev/null \
  | sort -n | tail -n 1
