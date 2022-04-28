import sys
import pprint
import re

# reports[id] = { orientation: 'xyz', points = [...] }
def get_reports(fh):
    reports = []
    scanner_id = None
    header = re.compile(r'^--- scanner ([0-9]+) ---$')
    for line in fh:
        line = line.strip()
        if len(line) == 0:
            continue
        else:
            m = header.match(line)
            if m is None:
                reports[scanner_id]['points'].append(tuple(line.split(',')))
            else:
                scanner_id = int(m.group(1))
                reports.append({'scanner_id': scanner_id,
                                'orientation': None,
                                'points': []})
    return reports


# Not straight line distance.
# Only makes sense for points of same orientation.
def distance(p1, p2):
    x1, y1, z1 = tuple(p1)
    x2, y2, z2 = tuple(p2)

    return abs((x1 - x2) + (y1 - y2) + (z1 - z2))


def find_beacons(reports, r=1000, req_match_count=12):

    return []

if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    reports_by_scanner = get_reports(sys.stdin)
    pp.pprint(reports_by_scanner)
    beacons = find_beacons(reports_by_scanner)
    pp.pprint(beacons)
