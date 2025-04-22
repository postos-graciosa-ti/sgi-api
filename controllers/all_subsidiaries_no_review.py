from datetime import datetime, timedelta

from sqlmodel import Session, select

from database.sqlite import engine
from models.subsidiarie import Subsidiarie
from models.workers import Workers
from models.workers_first_review import WorkersFirstReview
from models.workers_second_review import WorkersSecondReview
from pyhints.no_reviews import SubsidiaryFilter


def handle_get_workers_without_first_review_in_range_all(data: SubsidiaryFilter):
    subsidiaries_ids = data.subsidiaries_ids

    with Session(engine) as session:
        today = datetime.today()

        start_of_week = today - timedelta(days=today.weekday())

        end_of_week = start_of_week + timedelta(days=6)

        workers_without_first_review = (
            session.exec(
                select(
                    Workers.id.label("worker_id"),
                    Workers.name.label("worker_name"),
                    Workers.admission_date.label("worker_admission_date"),
                    Workers.first_review_date.label("worker_first_review_date"),
                    Subsidiarie.id.label("subsidiarie_id"),
                    Subsidiarie.name.label("subsidiarie_name"),
                )
                .join(Subsidiarie, Workers.subsidiarie_id == Subsidiarie.id)
                .where(Workers.first_review_date >= start_of_week)
                .where(Workers.first_review_date <= end_of_week)
                .where(~Workers.id.in_(select(WorkersFirstReview.worker_id)))
                .where(Workers.subsidiarie_id.in_(subsidiaries_ids))
            )
            .mappings()
            .all()
        )

        return workers_without_first_review


def handle_get_workers_without_second_review_in_range_all(data: SubsidiaryFilter):
    subsidiaries_ids = data.subsidiaries_ids

    with Session(engine) as session:
        today = datetime.today()

        start_of_week = today - timedelta(days=today.weekday())

        end_of_week = start_of_week + timedelta(days=6)

        workers_without_second_review = (
            session.exec(
                select(
                    Workers.id.label("worker_id"),
                    Workers.name.label("worker_name"),
                    Workers.admission_date.label("worker_admission_date"),
                    Workers.second_review_date.label("worker_second_review_date"),
                    Subsidiarie.id.label("subsidiarie_id"),
                    Subsidiarie.name.label("subsidiarie_name"),
                )
                .join(Subsidiarie, Workers.subsidiarie_id == Subsidiarie.id)
                .where(Workers.second_review_date >= start_of_week)
                .where(Workers.second_review_date <= end_of_week)
                .where(~Workers.id.in_(select(WorkersSecondReview.worker_id)))
                .where(Workers.subsidiarie_id.in_(subsidiaries_ids))
            )
            .mappings()
            .all()
        )

        return workers_without_second_review
