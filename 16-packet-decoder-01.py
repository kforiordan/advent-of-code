import sys
import pprint

class Header():
    version: int
    type_id: int

    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id

    def __repr__(self):
        return("Header({}, {})".format(self.version, self.type_id))


class Payload():
    nothing: str

    def __repr__(self):
        return('Payload()')


class Packet():
    header: Header
    payload: Payload

    def __init__(self, header, payload=None):
        if isinstance(header, Header):
            self.header = header
        else:
            if isinstance(header, list):
                self.header = Header(header[0], header[1])
            elif isinstance(header, tuple):
                v, t = header
                self.header = Header(v, t)
            else:
                self.header = "I am not adding exceptions, etc."

        if payload != None:
            self.payload = payload
            if isinstance(payload, list):
                self.payload = OperatorPayload(payload)
            else:
                self.payload = LiteralPayload(payload)

    def __repr__(self):
        return("Packet(version={}, type_id={}, payload={}".format(
            self.header.version, self.header.type_id, pp.pformat(self.payload)))

    def sub_packets(self):
        if isinstance(self.payload, OperatorPayload):
            return self.payload.sub_packets
        else:
            return[]

    def val(self):
        if isinstance(self.payload, LiteralPayload):
            return self.payload.v
        else:
            return None


class LiteralPayload(Packet):
    v: int

    def __init__(self, payload):
        self.v = payload

    def __repr__(self):
        return("LiteralPayload({})".format(self.v))


class OperatorPayload(Packet):
    sub_packets: list[Packet]

    def __init__(self, sub_packets):
        self.sub_packets = sub_packets

    def __repr__(self):
        return("OperatorPayload({})".format(', '.join(map(pp.pformat,self.sub_packets))))


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


def parse_literal_payload(bitq, idx):
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


def parse_operator_payload(bitq, idx):
    length_type_id = bitq[idx]
    idx += 1

    if length_type_id == '0':
        idx, payload = parse_operator_payload_type_zero(bitq, idx)
    else:
        idx, payload = parse_operator_payload_type_one(bitq, idx)

    return idx, payload


def parse_operator_payload_type_zero(bitq:list[str], idx:int) -> Payload:
    packets = []

    payload_len = 15
    bits = bitq[idx:(idx+payload_len)]
    idx += payload_len
    length_in_bits = int(''.join(bits), base=2)

    sub_bitq = bitq[idx:(idx+length_in_bits)]
    idx += length_in_bits
    sub_packets = parse_bitq(sub_bitq, 0, False)
    for p in sub_packets:
        packets.append(p)

    return idx, packets


def parse_operator_payload_type_one(bitq:list[str], idx:int) -> OperatorPayload:
    packets = []

    so_sick_of_naming_variables = 11
    bits = bitq[idx:(idx+so_sick_of_naming_variables)]
    idx += so_sick_of_naming_variables
    n_sub_packets = int(''.join(bits), base=2)

    for i in range(0, n_sub_packets):
        idx, sub_packets = parse_packet(bitq, idx)

    return idx, packets


# Returns a packet, which may itself contain sub packets.
def parse_packet(bitq:list[str], idx:int, zero_padded=False) -> Packet:
    packet = None
    idx, header = parse_header(bitq, idx)

    #print(" parse_packet: idx {}, header type {}".format(idx, header.type_id))
    payload = None
    if header.type_id == 4:
        parser = parse_literal_payload
    else:
        parser = parse_operator_payload
    idx, payload = parser(bitq, idx)
    packet = Packet(header, payload)

    #pp.pprint(packet)
    if zero_padded:
        n_bits_in_hex = 8  # Yeah, not 16.  Hahahahahah
        n_zeroes = (n_bits_in_hex - (idx % n_bits_in_hex)) % n_bits_in_hex
        for i in range(0, n_zeroes):
            if bitq[idx] != '0':
                print("You done goofed: {} {}/{}".format(idx, i, n_zeroes))
            idx += 1

    return idx, packet


def parse_bitq(bitq:list[str], idx:int=0, zero_padded=True) -> list[Packet]:
    packets = []

    n = len(bitq)
    while idx < n:
        #print("parse_bitq {}".format(idx))
        idx, packet = parse_packet(bitq, idx, zero_padded)
        packets.append(packet)

    return packets


def get_packets_as_bit_list(fh) -> list[str]:
    # Read hex from stdin, convert to bits and append to bitq
    for line in sys.stdin:
        #print(line)
        for c in list(line.strip()):
            b = bin(int(c, base=16))
            bits = list(b)[2:]	# Skip leading '0b'
            zero_padded = list(['0' for i in range(0,4-len(bits))] + bits)
            for d in zero_padded:
                bitq.append(d)


def get_all_version_numbers(packet):
    version_numbers = []

    version_numbers.append(packet.header.version)
    if packet.header.type_id != 4:
        for p in packet.sub_packets():
            n = get_all_version_numbers(p)
            for v in n:
                version_numbers.append(v)

    return(version_numbers)


def version_sum(packets):
    total = 0

    for p in packets:
        total += sum(get_all_version_numbers(p))

    return total


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    bitq = []	# Not really a queue
    packets = []

    get_packets_as_bit_list(sys.stdin)	# Updates bitq.  Ugh.

    packets = parse_bitq(bitq)

    print("Version sum: {}".format(version_sum(packets)))
