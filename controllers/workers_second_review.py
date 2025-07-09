from datetime import date, datetime, timedelta

from sqlmodel import Session, select

from database.sqlite import engine
from models.user import User
from models.workers import Workers
from models.workers_second_review import WorkersSecondReview


def handle_get_workers_without_second_review_in_range(subsidiarie_id: int):
    with Session(engine) as session:
        today = datetime.today()

        start_of_week = today - timedelta(days=today.weekday())

        end_of_week = start_of_week + timedelta(days=6)

        start_of_week_str = start_of_week.strftime("%Y-%m-%d")

        end_of_week_str = end_of_week.strftime("%Y-%m-%d")

        workers_without_second_review = session.exec(
            select(Workers)
            .where(Workers.subsidiarie_id == subsidiarie_id)
            .where(Workers.second_review_date >= start_of_week_str)
            .where(Workers.second_review_date <= end_of_week_str)
            .where(
                ~Workers.id.in_(
                    select(WorkersSecondReview.worker_id).where(
                        WorkersSecondReview.worker_id == Workers.id
                    )
                )
            )
        ).all()

        return {
            "workers": workers_without_second_review,
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
        }


def handle_get_workers_second_review(subsidiarie_id: int):
    with Session(engine) as session:
        today = date.today()

        start_of_week = (today - timedelta(days=today.weekday())).isoformat()

        end_of_week = (
            datetime.fromisoformat(start_of_week) + timedelta(days=6)
        ).isoformat()

        second_review_notifications = (
            session.exec(
                select(WorkersSecondReview, User, Workers)
                .join(User, WorkersSecondReview.realized_by == User.id)
                .join(Workers, WorkersSecondReview.worker_id == Workers.id)
                .where(Workers.subsidiarie_id == subsidiarie_id)
                .where(WorkersSecondReview.realized_in >= start_of_week)
                .where(WorkersSecondReview.realized_in <= end_of_week)
                .where(Workers.is_active == True)  # noqa: E712
                .where(Workers.is_away == False)  # noqa: E712
            )
            .mappings()
            .all()
        )

        return second_review_notifications


def handle_get_worker_second_review(id: int):
    with Session(engine) as session:
        db_worker_first_review = session.exec(
            select(WorkersSecondReview).where(WorkersSecondReview.worker_id == id)
        ).one()

        return db_worker_first_review


def handle_post_worker_second_review(
    id: int, worker_second_review: WorkersSecondReview
):
    worker_second_review.worker_id = id

    with Session(engine) as session:
        session.add(worker_second_review)

        session.commit()

        session.refresh(worker_second_review)

        return worker_second_review
