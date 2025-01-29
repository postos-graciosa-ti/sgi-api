from datetime import datetime, timedelta

from sqlmodel import Session, func, select

from database.sqlite import engine
from models.jobs import Jobs
from models.scale import Scale
from models.workers import Workers


async def get_workers_without_scales(subsidiarie_id):
    with Session(engine) as session:
        all_workers = session.exec(
            select(Workers).where(Workers.subsidiarie_id == subsidiarie_id)
        ).all()

        all_scales = session.exec(
            select(Scale).where(Scale.subsidiarie_id == subsidiarie_id)
        ).all()

        workers_with_scales = {scale.worker_id for scale in all_scales}

        workers_without_scale = [
            worker for worker in all_workers if worker.id not in workers_with_scales
        ]

        return workers_without_scale


async def get_workers_with_less_than_ideal_days_off(subsidiarie_id):
    with Session(engine) as session:
        today = datetime.now()

        year = today.year

        month = today.month

        first_day = datetime(year, month, 1)

        last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        sundays = 0

        current_day = first_day

        while current_day <= last_day:
            if current_day.weekday() == 6:
                sundays += 1
            current_day += timedelta(days=1)

        ideal_days_off = sundays + 4

        workers = session.exec(
            select(Workers)
            .join(Scale, Workers.id == Scale.worker_id)
            .where(Scale.subsidiarie_id == subsidiarie_id)
            .where(func.json_array_length(Scale.days_off) < ideal_days_off)
        ).all()

        return {"workers": workers, "ideal_days_off": ideal_days_off}


async def get_open_jobs(subsidiarie_id):
    with Session(engine) as session:
        jobs = session.exec(
            select(Jobs).where(Jobs.subsidiarie_id == subsidiarie_id)
        ).all()

        return jobs


async def handle_get_subsidiarie_notifications(id: int):
    workers_without_scales = await get_workers_without_scales(id)

    open_jobs = await get_open_jobs(id)

    workers_with_less_than_ideal_days_off = (
        await get_workers_with_less_than_ideal_days_off(id)
    )

    return {
        "workers_without_scales": workers_without_scales,
        "open_jobs": open_jobs,
        "workers_with_less_than_ideal_days_off": workers_with_less_than_ideal_days_off[
            "workers"
        ],
        "ideal_days_off": workers_with_less_than_ideal_days_off["ideal_days_off"],
    }
