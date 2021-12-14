import sys
import pprint
import copy


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
#        elif len(signal) == 7:
            # Must be number 8.  That's helpful.


def get_output_value(valid_segments, input_signals, output_signals):
    wire_to_segment_map = {k:valid_segments.copy() for k in valid_segments}
    pp.pprint(input_signals)
    pp.pprint(wire_to_segment_map)
    easy_ones_first(wire_to_segment_map, input_signals)
    pp.pprint(wire_to_segment_map)

    exit(0)
    return 0


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)
    input_signals = []
    output_signals = []
    segments = set('abcdefg')

    (input_signals, output_signals) = get_signals(sys.stdin)

    output_values = [get_output_value(segments, i,o) for (i,o) in
                     zip(input_signals, output_signals)]
    pp.pprint(output_signals)
    exit(0)

    print(sum(output_values))
