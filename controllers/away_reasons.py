from models.away_reasons import AwayReasons
from repositories.get_all_records import get_all_records


def handle_get_away_reasons():
    return get_all_records(AwayReasons)
