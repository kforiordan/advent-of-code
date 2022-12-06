#!/usr/bin/env python3

import sys


def get_message_buffers(fh):
    message_buffers = []	# Test data has four messages, prod has one.

    for line in fh:
        line = line.rstrip('\n')
        message_buffers.append(line)

    return message_buffers


def is_unique(s, flag_len=4):
    if len(s) != flag_len:
        print(f'flag length is {len(s)}, should be {flag_len}')
        return False

    i=0
    dup_found=False
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


if __name__ == "__main__":

    message_buffers = get_message_buffers(sys.stdin)

    flag_len = 4	# The flag is 4 consecutive unique chars
    for message_buffer in message_buffers:
        message_start_index = None
        buffer_len = len(message_buffer)
        i = 0
        while i < (buffer_len + flag_len - 1):
            if is_unique(message_buffer[i:i+flag_len]):
                message_start_index = i + flag_len
                break
            i += 1
        m = message_buffer[0:13]
        print(f'Silver: {m}... -> {message_start_index}')
