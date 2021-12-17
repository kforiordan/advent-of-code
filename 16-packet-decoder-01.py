import sys
import pprint

class Header():
    version: int
    type_id: int

    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id


class Packet():
    def __init__(self, header, payload=None):
        self.header = header
        if payload != None:
            self.payload = payload
    #     if sub_packets != None:
    #         self.sub_packets = sub_packets
    # , sub_packets=None):


class LiteralPacket(Packet):
    payload: int

    def __init__(self, payload):
        self.payload = payload

class OperatorPacket(Packet):
    sub_packets: [Packet]	# Is this right?

    def __init__(self, sub_packets):
        self.sub_packets = sub_packets


def parse_header(bitq, idx):
    #print("{}: {}".format(idx, ''.join(bitq[idx:(idx+6)])))
    version_len, type_id_len = 3, 3

    bits = bitq[idx:(idx+version_len)]
    idx += version_len
    version = int(''.join(bits), base=2)

    bits = bitq[idx:(idx+type_id_len)]
    idx += type_id_len
    type_id = int(''.join(bits), base=2)

    return idx, Header(version, type_id)


def parse_literal_packet_payload(bitq, idx):
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
        packets = parse_operator_packet_type_zero(bitq, idx)
    else:
        packets = parse_operator_packet_type_zero(bitq, idx)

    return idx, packets


def parse_operator_packet_type_zero(bitq, idx):
    packets = []

    so_sick_of_naming_variables = 15
    bits = bitq[idx:(idx+so_sick_of_naming_variables)]
    idx += so_sick_of_naming_variables
    length_in_bits = int(''.join(bits), base=2)

    sub_bitq = bitq[idx:(idx+length_in_bits)]
    idx += length_in_bits
    sub_packets = parse_bitq(sub_bitq, 0)
    for p in sub_packets:
        packets.append(p)

    return packets


def parse_operator_packet_type_one(bitq, idx):
    packets = []

    so_sick_of_naming_variables = 11
    bits = bitq[idx:(idx+so_sick_of_naming_variables)]
    idx += so_sick_of_naming_variables
    n_sub_packets = int(''.join(bits), base=2)

    for i in range(0, n_sub_packets):
        idx, sub_packets = parse_packet(bitq, idx)

    return idx, packets


# Despite the name, this returns a list of packets.
def parse_packet(bitq, idx, zero_padded=False):
    packets = []
    idx, header = parse_header(bitq, idx)

    #print(" parse_packet: idx {}, header type {}".format(idx, header.type_id))
    if header.type_id == 4:
        idx, packet = parse_literal_packet_payload(bitq, idx)
        packets.append(packet)
    else:
        idx, many_many_packets = parse_operator_packet(bitq, idx)
        for packet in many_many_packets:
            packets.append(packet)

    if zero_padded:
        n_bits_in_hex = 8  # Yeah, not 16.  Hahahahahah
        n_zeroes = (n_bits_in_hex - (idx % n_bits_in_hex)) % n_bits_in_hex
        for i in range(0, n_zeroes):
            if bitq[idx] != '0':
                print("You done goofed: {}".format(idx))
            idx += 1

    return idx, packets


def parse_bitq(bitq, idx=0):
    all_packets = []

    zero_padded = True

    n = len(bitq)
    while idx < n:
        #print("parse_bitq {}".format(idx))
        idx, packets = parse_packet(bitq, idx, zero_padded)
        for packet in packets:
            all_packets.append(packet)

    return all_packets


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
