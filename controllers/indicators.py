from sqlmodel import Session, select

from database.sqlite import engine
from models.indicators import Indicators, PostIndicatorsByMonthAndCriteria
from models.indicators_criteria import IndicatorsCriteria
from models.workers import Workers
from repositories.delete_record import delete_record
from repositories.get_all_records import get_all_records
from repositories.post_record import post_record


def handle_get_indicators():
    indicators = get_all_records(Indicators)

    with Session(engine) as session:
        result = [
            {
                "id": indicator.id,
                "month": indicator.month,
                "criteria": session.get(IndicatorsCriteria, indicator.criteria_id),
                "workers": [
                    session.get(Workers, worker_id)
                    for worker_id in eval(indicator.workers_ids)
                ],
                "note": indicator.note,
            }
            for indicator in indicators
        ]

    return result


def handle_get_indicators_by_month_and_criteria(body: PostIndicatorsByMonthAndCriteria):
    with Session(engine) as session:
        indicators = session.exec(
            select(Indicators)
            .where(Indicators.month == body.month)
            .where(Indicators.criteria_id == body.criteria_id)
        ).all()

        return indicators


def handle_post_indicators(indicator: Indicators):
    return post_record(indicator)


def handle_delete_indicators(id: int):
    return delete_record(Indicators, "id", id)
