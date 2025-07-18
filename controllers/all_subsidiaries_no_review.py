from datetime import date, datetime, timedelta

from sqlalchemy import and_, text
from sqlmodel import Session, select

from database.sqlite import engine
from models.subsidiarie import Subsidiarie
from models.workers import Workers
from models.workers_first_review import WorkersFirstReview
from models.workers_second_review import WorkersSecondReview
from pyhints.no_reviews import SubsidiaryFilter


async def handle_get_workers_without_first_review_in_range_all(data: SubsidiaryFilter):
    subsidiaries_ids = data.subsidiaries_ids

    with Session(engine) as session:
        today = datetime.today()

        start_of_week = (today - timedelta(days=today.weekday())).isoformat()

        end_of_week = (
            datetime.fromisoformat(start_of_week) + timedelta(days=6)
        ).isoformat()

        query = (
            select(
                Workers.id.label("worker_id"),
                Workers.name.label("worker_name"),
                Workers.admission_date.label("worker_admission_date"),
                Workers.first_review_date.label("worker_first_review_date"),
                Subsidiarie.id.label("subsidiarie_id"),
                Subsidiarie.name.label("subsidiarie_name"),
            )
            .join(Subsidiarie, Workers.subsidiarie_id == Subsidiarie.id)
            .where(text("workers.first_review_date >= :start_of_week"))
            .where(text("workers.first_review_date <= :end_of_week"))
            .where(~Workers.id.in_(select(WorkersFirstReview.worker_id)))
            .where(Workers.subsidiarie_id.in_(subsidiaries_ids))
            .where(Workers.is_active == True)  # noqa: E712
            .where(Workers.is_away == False)  # noqa: E712
        )

        workers_without_first_review = (
            session.exec(
                query.params(start_of_week=start_of_week, end_of_week=end_of_week)
            )
            .mappings()
            .all()
        )

        return {
            "workers": workers_without_first_review,
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
        }


async def handle_get_workers_without_second_review_in_range_all(data: SubsidiaryFilter):
    subsidiaries_ids = data.subsidiaries_ids

    with Session(engine) as session:
        today = datetime.today()

        start_of_week = (today - timedelta(days=today.weekday())).isoformat()

        end_of_week = (
            datetime.fromisoformat(start_of_week) + timedelta(days=6)
        ).isoformat()

        query = (
            select(
                Workers.id.label("worker_id"),
                Workers.name.label("worker_name"),
                Workers.admission_date.label("worker_admission_date"),
                Workers.second_review_date.label("worker_second_review_date"),
                Subsidiarie.id.label("subsidiarie_id"),
                Subsidiarie.name.label("subsidiarie_name"),
            )
            .join(Subsidiarie, Workers.subsidiarie_id == Subsidiarie.id)
            .where(text("workers.second_review_date >= :start_of_week"))
            .where(text("workers.second_review_date <= :end_of_week"))
            .where(~Workers.id.in_(select(WorkersSecondReview.worker_id)))
            .where(Workers.subsidiarie_id.in_(subsidiaries_ids))
            .where(Workers.is_active == True)  # noqa: E712
            .where(Workers.is_away == False)  # noqa: E712
        )

        workers_without_second_review = (
            session.exec(
                query.params(start_of_week=start_of_week, end_of_week=end_of_week)
            )
            .mappings()
            .all()
        )

        return {
            "workers": workers_without_second_review,
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
        }


def handle_get_away_return_workers(data: SubsidiaryFilter):
    today = date.today()

    start_of_week = today - timedelta(days=today.weekday())

    end_of_week = start_of_week + timedelta(days=6)

    with Session(engine) as session:
        workers_away_return = session.exec(
            select(Workers).where(
                and_(
                    Workers.subsidiarie_id.in_(data.subsidiaries_ids),
                    Workers.is_away.is_(True),
                    Workers.away_end_date >= start_of_week,
                    Workers.away_end_date <= end_of_week,
                )
            )
        ).all()

    return {
        "workers": workers_away_return,
        "start_of_week": start_of_week,
        "end_of_week": end_of_week,
    }
