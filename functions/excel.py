import re
from datetime import time


def convert_to_time(time_string):
    if time_string:
        return time(*map(int, time_string.split(":")))

    return time(0, 0)


def extract_turn_info(turn_string):
    pattern = r"(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})"

    match = re.match(pattern, turn_string)

    if match:
        start_time = match.group(1)

        end_time = match.group(2)

        return (
            start_time,
            None,
            end_time,
            None,
        )

    return None, None, None, None
