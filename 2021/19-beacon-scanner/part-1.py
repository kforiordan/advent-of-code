import sys
import pprint
import re

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
                reports[scanner_id].append(line.split(','))
            else:
                scanner_id = int(m.group(1))
                reports.append([])
    return reports

if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    reports_by_scanner = get_reports(sys.stdin)
    pp.pprint(reports_by_scanner)
