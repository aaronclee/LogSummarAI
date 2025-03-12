import re
from datetime import datetime

def parse_log_line(line):
    """
    Parses a log line into a structured dictionary.
    Expected format: 
      2025-03-11 01:13:20.130 [info] [module] Message text...
    """
    pattern = r"^\[(.*?)\]\s+(\w+):\s+(.*)$"
    match = re.match(pattern, line)
    if match:
        timestamp_str, level, message = match.groups()
        # Parse the timestamp; adjust the format if needed.
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If the timestamp includes milliseconds, try another format.
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        return {"timestamp": timestamp, "level": level.upper(), "message": message}
    else:
        return None
    