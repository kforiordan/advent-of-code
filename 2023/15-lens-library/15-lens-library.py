#!/usr/bin/env python3

import sys

def get_init_seq(fh):
    steps = []
    for line in fh:
        for step in line.rstrip().split(','):
            steps.append(step)
    return steps


def hash(s):
    v = 0
    for c in s:
        v += ord(c)
        v = v * 17
        v = v % 256
    return v


def hash_steps(steps):
    return [hash(s) for s in steps]


def parse_step(step):
    label, op, arg = [], None, None
    for c in step:
        if (ord(c) >= ord('a') and ord(c) <= ord('z')) or \
           (ord(c) >= ord('A') and ord(c) <= ord('Z')):
            label.append(c)
        elif c in '-=':
            op = c
        elif c in '0123456789':
            arg = int(c)
        else:
            print("wat is '{}'".format(step))
            exit(0)

    return ("".join(label), op, arg)


def put_lenses_in_boxes(steps):
    boxes = [None for _ in range(256)]
    for s in steps:
        label, op, focal_length = parse_step(s)
        box = boxes[hash(label)]
        if box == None:
            if op == '=':
                box = {}
                lens = {
                    'focal_length':focal_length,
                    'position': 0
                }
                box['lenses'] = {label: lens}
                box['next_position'] = lens['position'] + 1
            elif op == '-':
                continue
        else:
            if op == '=':
                if label in box['lenses']:
                    box['lenses'][label]['focal_length'] = focal_length
                else:
                    box['lenses'][label] = {
                        'focal_length':focal_length,
                        'position':box['next_position']
                    }
                    box['next_position'] += 1
            elif op == '-':
                if label in box['lenses']:
                    del(box['lenses'][label])
                else:
                    continue
        boxes[hash(label)] = box
    return boxes


def gold(steps):
    boxes = put_lenses_in_boxes(steps)

    for i,box in enumerate(boxes):
        if box != None:
            lens_string = ", ".join(box['lenses'].keys())
#            print("Box {}: {}".format(i, lens_string))
    focal_length_power_sum = 0

    for i,box in enumerate(boxes):
        if box != None:
            f = lambda x: box['lenses'][x]['position']
            for j,lens in enumerate(sorted(box['lenses'].keys(), key=f)):
                power = (i+1) * (j+1) * box['lenses'][lens]['focal_length']
                focal_length_power_sum += power

    return focal_length_power_sum


if __name__ == "__main__":
    steps = get_init_seq(sys.stdin)
    print("Silver: {}".format(sum(hash_steps(steps))))
    print("Gold: {}".format(gold(steps)))

