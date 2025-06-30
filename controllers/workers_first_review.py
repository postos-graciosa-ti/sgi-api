from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from sqlmodel import Session, select

from database.sqlite import engine
from models.user import User
from models.workers import Workers
from models.workers_first_review import WorkersFirstReview


def handle_get_workers_without_first_review_in_range(subsidiarie_id: int):
    with Session(engine) as session:
        today = datetime.today()

        start_of_week = today - relativedelta(days=today.weekday())

        end_of_week = start_of_week + relativedelta(days=6)

        start_of_week_str = start_of_week.strftime("%Y-%m-%d")

        end_of_week_str = end_of_week.strftime("%Y-%m-%d")

        workers_without_first_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.first_review_date >= start_of_week_str)
            .where(Workers.first_review_date <= end_of_week_str)
            .where(
                ~Workers.id.in_(
                    select(WorkersFirstReview.worker_id).where(
                        WorkersFirstReview.worker_id == Workers.id
                    )
                )
            )
        ).all()

        return {
            "workers": workers_without_first_review,
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
        }


def handle_get_workers_first_review(subsidiarie_id: int):
    with Session(engine) as session:
        today = date.today()

        start_of_week = (today - timedelta(days=today.weekday())).isoformat()

        end_of_week = (
            datetime.fromisoformat(start_of_week) + timedelta(days=6)
        ).isoformat()

        first_review_notifications = (
            session.exec(
                select(WorkersFirstReview, User, Workers)
                .join(User, WorkersFirstReview.realized_by == User.id)
                .join(Workers, WorkersFirstReview.worker_id == Workers.id)
                .where(Workers.subsidiarie_id == subsidiarie_id)
                .where(WorkersFirstReview.realized_in >= start_of_week)
                .where(WorkersFirstReview.realized_in <= end_of_week)
            )
            .mappings()
            .all()
        )

        return first_review_notifications


def handle_get_worker_first_review(id: int):
    with Session(engine) as session:
        db_worker_first_review = session.exec(
            select(WorkersFirstReview).where(WorkersFirstReview.worker_id == id)
        ).one()

        return db_worker_first_review


def handle_post_worker_first_review(id: int, worker_first_review: WorkersFirstReview):
    worker_first_review.worker_id = id

    with Session(engine) as session:
        session.add(worker_first_review)

        session.commit()

        session.refresh(worker_first_review)

        return worker_first_review
