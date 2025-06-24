from models.indicators import Indicators
from repositories.get_all_records import get_all_records
from repositories.post_record import post_record


def handle_get_indicators():
    return get_all_records(Indicators)


def handle_post_indicators(indicator: Indicators):
    return post_record(indicator)
