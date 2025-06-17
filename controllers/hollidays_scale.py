import json

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlmodel import Session, select

from database.sqlite import engine
from models.hollidays_scale import HollidaysScale
from models.workers import Workers


def handle_get_holliday_schedule(id: int, date: str):
    with Session(engine) as session:
        db_holliday = session.exec(
            select(HollidaysScale)
            .where(HollidaysScale.subsidiarie_id == id)
            .where(HollidaysScale.date == date)
        ).first()

        result = {
            "id": db_holliday.id,
            "subsidiarie_id": db_holliday.subsidiarie_id,
            "date": db_holliday.date,
            "working": json.loads(db_holliday.working),
            "resting": json.loads(db_holliday.resting),
        }

        return result


def handle_post_holliday_schedule(holliday_schedule: HollidaysScale):
    with Session(engine) as session:
        existing = session.exec(
            select(HollidaysScale)
            .where(HollidaysScale.subsidiarie_id == holliday_schedule.subsidiarie_id)
            .where(HollidaysScale.date == holliday_schedule.date)
        ).first()

        if existing:
            existing.working = holliday_schedule.working

            existing.resting = holliday_schedule.resting

            session.add(existing)

        else:
            session.add(holliday_schedule)

        session.commit()

        return {"success": True}
