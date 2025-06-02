from fastapi import HTTPException
from sqlmodel import Session, select

from database.sqlite import engine
from models.workers_pictures import WorkersPictures


def handle_get_workers_pictures(worker_id: int):
    with Session(engine) as session:
        worker_pictures = session.exec(
            select(WorkersPictures).where(WorkersPictures.worker_id == worker_id)
        ).all()

        if len(worker_pictures) > 1:
            raise HTTPException(
                status_code=404, detail="Colaborador já possui uma foto"
            )
        else:
            return worker_pictures[0]


def handle_post_workers_pictures(body: WorkersPictures):
    with Session(engine) as session:
        session.add(body)

        session.commit()

        session.refresh(body)

        return body


def handle_delete_workers_pictures(worker_id: int):
    with Session(engine) as session:
        worker_picture = session.exec(
            select(WorkersPictures).where(WorkersPictures.worker_id == worker_id)
        ).first()

        session.delete(worker_picture)

        session.commit()

        return {"success": True}
