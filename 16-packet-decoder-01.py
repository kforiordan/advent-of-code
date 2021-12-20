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

    return idx, numbers


def parse_operator_packet(bitq, idx):
    packets = []

    return idx, packets


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
