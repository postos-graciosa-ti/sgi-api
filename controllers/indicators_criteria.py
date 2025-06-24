from models.indicators_criteria import IndicatorsCriteria
from repositories.delete_record import delete_record
from repositories.get_all_records import get_all_records
from repositories.patch_record import patch_record
from repositories.post_record import post_record


def handle_get_indicators_criteria():
    return get_all_records(IndicatorsCriteria)


def handle_post_indicators_criteria(indicator_criteria: IndicatorsCriteria):
    return post_record(indicator_criteria)


def handle_patch_indicators_criteria(id: int, indicator_criteria: IndicatorsCriteria):
    updates = {"name": indicator_criteria.name}

    result = patch_record(
        model=IndicatorsCriteria,
        pk_column="id",
        pk_column_value=id,
        updates=updates,
    )

    return result


def handle_delete_indicators_criteria(id: int):
    return delete_record(IndicatorsCriteria, "id", id)
