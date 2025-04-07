from sqlmodel import Session, select

from database.sqlite import engine
from models.workers_second_review import WorkersSecondReview


def handle_get_worker_first_review(id: int):
    with Session(engine) as session:
        db_worker_first_review = session.exec(
            select(WorkersSecondReview).where(WorkersSecondReview.worker_id == id)
        ).one()

        return db_worker_first_review
