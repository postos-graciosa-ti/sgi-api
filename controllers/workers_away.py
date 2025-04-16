from datetime import datetime

from sqlmodel import Session, select

from database.sqlite import engine
from models.workers import Workers
from pyhints import WorkersAway


def handle_worker_away(subsidiarie_id: int, worker_id: int, worker: WorkersAway):
    with Session(engine) as session:
        get_db_worker = (
            select(Workers)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        )

        db_worker = session.exec(get_db_worker).first()

        db_worker.is_away = True

        db_worker.away_start_date = (
            worker.away_start_date
            if worker.away_start_date
            else db_worker.away_start_date
        )

        db_worker.away_end_date = (
            worker.away_end_date if worker.away_end_date else db_worker.away_end_date
        )

        db_worker.away_reason_id = (
            worker.away_reason_id if worker.away_reason_id else db_worker.away_reason_id
        )

        start_date = datetime.strptime(worker.away_start_date, "%Y-%m-%d").date()

        end_date = datetime.strptime(worker.away_end_date, "%Y-%m-%d").date()

        away_days = (end_date - start_date).days + 1

        db_worker.time_away = away_days

        session.add(db_worker)

        session.commit()

        session.refresh(db_worker)

        return db_worker


def handle_worker_away_return(subsidiarie_id: int, worker_id: int):
    with Session(engine) as session:
        get_db_worker = (
            select(Workers)
            .where(Workers.id == worker_id)
            .where(Workers.subsidiarie_id == subsidiarie_id)
        )

        db_worker = session.exec(get_db_worker).first()

        db_worker.is_away = False

        session.add(db_worker)

        session.commit()

        return db_worker
