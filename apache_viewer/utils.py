import re
from datetime import datetime


def parse_apache_string(log):
    format_pat = re.compile(
        r"(?P<ip>(?:[\d\.]|[\da-fA-F:])+)\s"
        r"(?P<identity>\S*)\s"
        r"(?P<user>\S*)\s"
        r"\[(?P<time>.*?)\]\s"
        r"\"(?P<request_method>.*?) (?P<path>.*?)(?P<request_version>HTTP/.*)?\"\s"
        r"(?P<status>\d+)\s"
        r"(?P<bytes>\S*)\s"
        r'"(?P<referer>.*?)"\s'
        r'"(?P<user_agent>.*?)"\s*'
    )
    parser = format_pat.match(log)
    if parser is not None:
        return parser.groupdict()

    return False


def format_date(tms):
    return datetime.strptime(tms, "%d/%b/%Y:%H:%M:%S %z")
