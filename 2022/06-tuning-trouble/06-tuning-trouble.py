#!/usr/bin/env python3

import sys


def get_message_buffers(fh):
    return [line.rstrip('\n') for line in fh]


def is_unique(s, flag_len=4):
    dup_found=False
    i=0
    while i < flag_len:
        j=i+1
        while j < flag_len:
            if s[i] == s[j]:
                dup_found = True
                break
            j += 1
        if dup_found:
            break
        i += 1

    return not dup_found


def find_start(message_buffer, flag_len=4):
    message_start_index = None
    buffer_len = len(message_buffer)
    i = 0
    while i < (buffer_len + flag_len - 1):
        if is_unique(message_buffer[i:i+flag_len], flag_len):
            message_start_index = i + flag_len
            break
        i += 1

    return message_start_index


if __name__ == "__main__":
    message_buffers = get_message_buffers(sys.stdin)
    silver_flag_len = 4
    gold_flag_len = 14

    for mb in message_buffers:
        start = find_start(mb, silver_flag_len)
        print(f'Silver: {mb[0:13]}... -> {start}')

    for mb in message_buffers:
        start = find_start(mb, gold_flag_len)
        print(f'Gold: {mb[0:13]}... -> {start}')
