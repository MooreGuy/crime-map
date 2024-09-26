import re
import datetime


def parse_log(log_contents):
    separator = '={79}'
    lines = re.split(separator, log_contents)
    combined = combine_header_body(lines)
    return map(parse_entry, combined)


address_pattern = re.compile(r"Addr: (.*)Clearance Code")
date_pattern = re.compile(r"[0-9]+\s([0-9\/]+)\s")

simple_fields = {
    'report_number': re.compile(r"([0-9]+)\s"),
    'received': re.compile(r"Received:([0-9]{2}:[0-9]{2})\s"),
    'dispatched': re.compile(r"Dispatched:([0-9]{2}:[0-9]{2})\s"),
    'arrived': re.compile(r"Arrived:([0-9]{2}:[0-9]{2})\s"),
    'cleared': re.compile(r"Cleared:([0-9]{2}:[0-9]{2})\s"),
    'type': re.compile(r"Type:\s*([a-zA-Z0-9]+)"),
    'location': re.compile(r"Location:(\S*)"),
    'grid': re.compile(r"; GRID (.*)(,|;)"),
    'clearance_code': re.compile(r"Clearance Code: (\S*)\s"),
    'responsible_officer': re.compile(r"Responsible Officer: (\S*, .)"),
    "call_comments": re.compile(r"CALL COMMENTS: (.*)\n"),
    "description": re.compile(r"Des:(.*)incid"),
}


def parse_entry(line):
    entry = {'raw': line}

    if match := date_pattern.search(line):
        dateString = match.group(1)
        entry["date"] = dateString
        month, day, yearSmall = re.split(r"\/", dateString)
        year = f"20{yearSmall}"
        date = datetime.datetime(int(year), int(month), int(day))
        timestamp = date.timestamp()
        entry["timestamp"] = int(timestamp)

    if search := address_pattern.search(line):
        address_line = search.group(1)
        address_sections = re.split(";", address_line)
        entry["address"] = address_sections[0]

    for field_name in simple_fields:
        regex = simple_fields[field_name]
        if search := regex.search(line):
            entry[field_name] = search.group(1)

    return entry


# It's hard to split on every nth occurrence so splitting up the header and
# body and then recombining is how I decided to shortcut that.
def combine_header_body(lines):
    combined_lines = []
    header = ""
    body_pattern = re.compile(r'Type:\s')
    header_pattern = re.compile(r".*Received:.*Dispatched:")
    total = 0
    for line in lines:
        if body_match := body_pattern.search(line):
            total += 1
            event = header + line
            combined_lines.append(event)
        elif header_match := header_pattern.search(line):
            header = line

    return combined_lines
