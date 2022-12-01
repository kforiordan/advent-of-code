#!/bin/bash
sed 's/$/ +/;s/^[ +]*$/pc/' | dc 2>/dev/null \
  | sort -n | tail -n 3 \
  | (sed 's/$/ +/';echo p;) | dc 2>/dev/null
