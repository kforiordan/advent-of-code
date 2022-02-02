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
                reports[scanner_id]['points'].append(line.split(','))
            else:
                scanner_id = int(m.group(1))
                reports.append({'scanner_id': scanner_id,
                                'orientation': None,
                                'points': []})
    return reports

def find_beacons(reports, r=1000, req_match_count=12):
    return []

if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    reports_by_scanner = get_reports(sys.stdin)
    beacons = find_beacons(reports_by_scanner)
    pp.pprint(beacons)
