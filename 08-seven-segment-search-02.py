import sys
import pprint
import copy

# "... For each display, you watch the changing signals for a while,
# make a note of all ten unique signal patterns you see ..."


def get_signals(fh):
    for line in fh:
        signals = line.strip().split()
        input_signals.append(list(map(set,signals[0:10])))
        output_signals.append(list(map(set,signals[11:15])))

    return (input_signals, output_signals)


def easy_ones_first(wire_to_segment_map, input_signals):
    for signal in input_signals:
        if len(signal) == 2:
            segment_one = set('cf')
            # Must be number 1
            for wire in signal:
                for w in wire_to_segment_map:
                    if w in signal:
                        wire_to_segment_map[w] = \
                            wire_to_segment_map[w] & segment_one
                    else:
                        wire_to_segment_map[w] = \
                            wire_to_segment_map[w] - segment_one
        elif len(signal) == 3:
            # Must be number 7
            segment_seven = set('acf')
            for wire in signal:
                for w in wire_to_segment_map:
                    if w in signal:
                        wire_to_segment_map[w] = \
                            wire_to_segment_map[w] & segment_seven
                    else:
                        wire_to_segment_map[w] = \
                            wire_to_segment_map[w] - segment_seven
        elif len(signal) == 4:
            # Must be number 4
            segment_four = set('bcdf')
            for wire in signal:
                for w in wire_to_segment_map:
                    if w in signal:
                        wire_to_segment_map[w] = \
                            wire_to_segment_map[w] & segment_four
                    else:
                        wire_to_segment_map[w] = \
                            wire_to_segment_map[w] - segment_four
        # elif len(signal) == 7:
            # Must be number 8.  That's helpful.


def fivesandsixes(wire_to_segment_map, input_signals):
    one = [s for s in input_signals if len(s) == 2][0]
    four = [s for s in input_signals if len(s) == 4][0]
    seven = [s for s in input_signals if len(s) == 3][0]
    eight = [s for s in input_signals if len(s) == 7][0]

    two, three, five = None, None, None
    six, nine, zero = None, None, None

    twothreefive = [s for s in input_signals if len(s) == 5]
    sixninezero = [s for s in input_signals if len(s) == 6]
    twofive, sixzero = None, None

    # Identify three - it can be picked out of its trio
    ncommoneq = lambda a, b, q: len(a & b) == q
    if ncommoneq(twothreefive[0], twothreefive[1], 3):
        three = twothreefive[2]
        twofive = [twothreefive[0], twothreefive[1]]
    elif ncommoneq(twothreefive[0], twothreefive[2], 3):
        three = twothreefive[1]
        twofive = [twothreefive[0], twothreefive[2]]
    else:
        three = twothreefive[0]
        twofive = [twothreefive[1], twothreefive[2]]

    # Identify nine - it's the same set as three union four
    if sixninezero[0] == three.union(four):
        nine = sixninezero[0]
        sixzero = [sixninezero[1], sixninezero[2]]
    elif sixninezero[1] == three.union(four):
        nine = sixninezero[1]
        sixzero = [sixninezero[0], sixninezero[2]]
    else:
        nine = sixninezero[2]
        sixzero = [sixninezero[0], sixninezero[1]]

    # Identify two and five via their commonality with nine
    if ncommoneq(twofive[0], nine, 4):
        two = twofive[0]
        five = twofive[1]
    else:
        two = twofive[1]
        five = twofive[0]

    # The union of five and six is the same as six
    if sixzero[0] == five.union(sixzero[0]):
        six = sixzero[0]
        zero = sixzero[1]
    else:
        six = sixzero[1]
        zero = sixzero[0]

    # Knowing zero we can determine which wire corresponds to segment d
    segment_d_wire = eight ^ zero
    for w in wire_to_segment_map:
        if w in segment_d_wire:
            wire_to_segment_map[w] = set('d')
        else:
            wire_to_segment_map[w] = wire_to_segment_map[w] - set('d')

    # Knowing six we can determine which wire corresponds to segment c
    # (incidentally this also determines the segment f wire)
    segment_c_wire = eight ^ six
    for w in wire_to_segment_map:
        if w in segment_c_wire:
            wire_to_segment_map[w] = set('c')
        else:
            wire_to_segment_map[w] = wire_to_segment_map[w] - set('c')

    # Knowing nine we can determine which wire corresponds to segment e
    # (incidentally this also determines the segment g wire)
    segment_e_wire = eight ^ nine
    for w in wire_to_segment_map:
        if w in segment_e_wire:
            wire_to_segment_map[w] = set('e')
        else:
            wire_to_segment_map[w] = wire_to_segment_map[w] - set('e')




def signal_to_value(wire_to_segment_map, signal):
    segment_to_wire_map = {v:k for k, v in wire_to_segment_map.items()}

    if len(signal) == 2:
        return 1
    elif len(signal) == 3:
        return 7
    elif len(signal) == 4:
        return 4
    elif len(signal) == 7:
        return 8
    elif len(signal) == 5:
        if segment_to_wire_map['c'] in signal:
            if segment_to_wire_map['e'] in signal:
                return 2
            else:
                return 3
        else:
            return 5
    elif len(signal) == 6:
        if segment_to_wire_map['d'] in signal:
            if segment_to_wire_map['c'] in signal:
                return 9
            else:
                return 6
        else:
            return 0


    # This is an error state.  It should never be reached.  I'm not
    # handling it anyway.
    return -1



def unscramble_wire_to_segment_map(wire_to_segment_map, input_signals):

    easy_ones_first(wire_to_segment_map, input_signals)

    # This is the ugly function that does all the donkey work.  With
    # all the competence of a donkey performing set operations too.
    fivesandsixes(wire_to_segment_map, input_signals)

    for w,s in wire_to_segment_map.items():
        if len(s) == 1:
            wire_to_segment_map[w] = list(s)[0]
        else:
            # This is an error state.  I am not handling it though.
            False


def get_output_value(valid_segments, input_signals, output_signals):
    wire_to_segment_map = {k:valid_segments.copy() for k in valid_segments}
    output_digits = []
    output_value = 0

    unscramble_wire_to_segment_map(wire_to_segment_map, input_signals)

    for o in output_signals:
        output_digits.append(signal_to_value(wire_to_segment_map, o))

    e = 0
    for d in reversed(output_digits):
        output_value += d * (10 ** e)
        e += 1

    return output_value


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)
    input_signals = []
    output_signals = []
    segments = set('abcdefg')	# Also the number eight.

    (input_signals, output_signals) = get_signals(sys.stdin)

    output_values = [get_output_value(segments, i,o) for (i,o) in
                     zip(input_signals, output_signals)]

    print(sum(output_values))
