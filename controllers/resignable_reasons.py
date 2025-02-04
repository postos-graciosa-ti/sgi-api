import json
from datetime import datetime

from sqlmodel import Session, and_, select

from database.sqlite import engine
from models.resignable_reasons import ResignableReasons
from models.workers import Workers
from pyhints.resignable_reasons import StatusResignableReasonsInput


async def handle_get_resignable_reasons():
    with Session(engine) as session:
        resignable_reasons = session.exec(select(ResignableReasons)).all()

    return resignable_reasons


async def handle_resignable_reasons_report(input: StatusResignableReasonsInput):
    with Session(engine) as session:
        first_day = datetime.strptime(input.first_day, "%d-%m-%Y")

        last_day = datetime.strptime(input.last_day, "%d-%m-%Y")

        resignable_reasons_ids = json.loads(input.resignable_reasons_ids)

        if 0 in resignable_reasons_ids:
            resignable_reasons_ids = [
                reason for reason in session.exec(select(ResignableReasons.id)).all()
            ]

        stmt = (
            select(
                Workers.id.label("worker_id"),
                Workers.name.label("worker_name"),
                Workers.resignation_date,
                ResignableReasons.id.label("resignable_reason_id"),
                ResignableReasons.name.label("resignable_reason_name"),
            )
            .join(
                ResignableReasons,
                Workers.resignation_reason_id == ResignableReasons.id,
            )
            .where(
                and_(
                    Workers.resignation_reason_id.in_(resignable_reasons_ids),
                    Workers.resignation_date != None,
                )
            )
        )

        workers = session.exec(stmt).all()

        results = [
            {
                "worker_id": worker.worker_id,
                "worker_name": worker.worker_name,
                "resignation_date": worker.resignation_date,
                "resignable_reason_id": worker.resignable_reason_id,
                "resignable_reason_name": worker.resignable_reason_name,
            }
            for worker in workers
            if first_day
            <= datetime.strptime(worker.resignation_date, "%d-%m-%Y")
            <= last_day
        ]

    return results
