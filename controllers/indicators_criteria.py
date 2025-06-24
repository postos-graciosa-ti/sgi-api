from models.indicators_criteria import IndicatorsCriteria
from repositories.get_all_records import get_all_records
from repositories.post_record import post_record


def handle_get_indicators_criteria():
    return get_all_records(IndicatorsCriteria)


def handle_post_indicators_criteria(indicator_criteria: IndicatorsCriteria):
    return post_record(indicator_criteria)
