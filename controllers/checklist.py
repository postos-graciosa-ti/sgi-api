from fastapi import HTTPException
from sqlmodel import Session, select

from database.sqlite import engine
from models.checklist import Checklist, ChecklistCreate, ChecklistUpdate


def handle_get_checklist_by_worker(worker_id: int):
    with Session(engine) as session:
        statement = select(Checklist).where(Checklist.worker_id == worker_id)

        result = session.exec(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="Checklist not found")

        return result


def handle_create_checklist(checklist: ChecklistCreate):
    with Session(engine) as session:
        exists = session.exec(
            select(Checklist).where(Checklist.worker_id == checklist.worker_id)
        ).first()

        if exists:
            raise HTTPException(
                status_code=400, detail="Checklist for this worker already exists"
            )

        db_checklist = Checklist.from_orm(checklist)

        session.add(db_checklist)

        session.commit()

        session.refresh(db_checklist)

        return db_checklist


def handle_patch_checklist(checklist_id: int, checklist_update: ChecklistUpdate):
    with Session(engine) as session:
        checklist = session.get(Checklist, checklist_id)

        if not checklist:
            raise HTTPException(status_code=404, detail="Checklist not found")

        update_data = checklist_update.dict(exclude_unset=True)

        update_data.pop("worker_id", None)

        for key, value in update_data.items():
            setattr(checklist, key, value)

        session.add(checklist)

        session.commit()

        session.refresh(checklist)

        return checklist
