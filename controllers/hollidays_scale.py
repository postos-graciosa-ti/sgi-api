from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlmodel import Session, select

from database.sqlite import engine
from models.hollidays_scale import HollidaysScale
from models.workers import Workers


def handle_get_hollidays_scale(id: int, date: str):
    with Session(engine) as session:
        holliday_scale_by_date = session.exec(
            select(HollidaysScale)
            .where(HollidaysScale.subsidiarie_id == id)
            .where(HollidaysScale.date == date)
        ).all()

        return [
            {
                "id": scale.id,
                "date": scale.date,
                "worker": session.get(Workers, scale.worker_id),
            }
            for scale in holliday_scale_by_date
        ]


def handle_post_hollidays_scale(holliday_scale: HollidaysScale):
    with Session(engine) as session:
        holliday_scale_penalty = session.exec(
            select(HollidaysScale)
            .where(HollidaysScale.subsidiarie_id == holliday_scale.subsidiarie_id)
            .where(HollidaysScale.worker_turn_id == holliday_scale.worker_turn_id)
            .where(
                HollidaysScale.worker_function_id == holliday_scale.worker_function_id
            )
            .where(HollidaysScale.date == holliday_scale.date)
        ).all()

        if len(holliday_scale_penalty) > 0:
            raise HTTPException(
                status_code=400,
                detail="Já existe um colaborador do mesmo turno e função de folga no mesmo dia.",
            )

        session.add(holliday_scale)

        session.commit()

        session.refresh(holliday_scale)

        return holliday_scale


def handle_delete_hollidays_scale(id: int):
    with Session(engine) as session:
        holliday_scale = session.exec(
            select(HollidaysScale).where(HollidaysScale.id == id)
        ).first()

        session.delete(holliday_scale)

        session.commit()

        return {"success": True}
