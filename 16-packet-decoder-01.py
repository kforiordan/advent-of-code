import sys
import pprint

class Header():
    version: int
    type_id: int

    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id


def parse_header(bitq, idx):
    version_len, type_id_len = 3, 3

    bits = bitq[idx:(idx+version_len)]
    idx += version_len
    version = int(''.join(bitq[idx:(idx+version_len)]), base=2)

    bits = bitq[idx:(idx+type_id_len)]
    idx += type_id_len
    type_id = int(''.join(bits), base=2)

    return idx, Header(version, type_id)


def parse_literal_packet(bitq, idx):
    data_len = 4

    numbers = []
    while True:
        flag = bitq[idx]
        idx += 1

        bits = bitq[idx:(idx+data_len)]
        idx += data_len
        numbers.append(int(''.join(bits), base=2))

        if flag == '0':
            break

    literal_goddamn_number = 0
    for e,d in enumerate(reversed(numbers)):
        literal_goddamn_number += (d * (16 ** e))

    return idx, literal_goddamn_number


def parse_operator_packet(bitq, idx):
    packets = []

    length_type_id = bitq[idx]
    idx += 1

    if length_type_id == '0':
        packets = parse_operator_packet_type_one(bitq, idx)
    else:
        packets = parse_operator_packet_type_one(bitq, idx)

    return idx, packets


def parse_operator_packet_type_one(bitq, idx):
    packets = []

    so_sick_of_naming_variables = 15
    bits = bitq[idx:(idx+so_sick_of_naming_variables)]
    idx += so_sick_of_naming_variables
    length_in_bits = int(''.join(bits), base=2)

    sub_bitq = bitq[idx:(idx+length_in_bits)]
    idx += length_in_bits
    sub_packets = parse_packets(sub_bitq, 0)
    for p in sub_packets:
        packets.append(p)

    return packets



def parse_bitq(bitq, idx=0):
    packets = []

    idx, header = parse_header(bitq, idx)
    n = len(bitq)
    while idx < n:
        if header.type_id == 4:
            idx, packet = parse_literal_packet(bitq, idx)
            packets.append(packet)
        else:
            idx, many_many_packets = parse_operator_packet(bitq, idx)
            for packet in many_many_packets:
                packets.append(packet)

    return packets


def get_packets_as_bit_list(fh):
    # Read hex from stdin, convert to bits and append to bitq
    for line in sys.stdin:
        for c in list(line.strip()):
            b = bin(int(c, base=16))
            bits = list(b)[2:]	# Skip leading '0b'
            zero_padded = list(['0' for i in range(0,4-len(bits))] + bits)
            for d in zero_padded:
                bitq.append(d)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    bitq = []	# Yes, I know python lists are poor queues.
    packets = []

    get_packets_as_bit_list(sys.stdin)	# Updates bitq.  Ugh.

    packets = parse_bitq(bitq)
