from sqlmodel import Session, select

from database.sqlite import engine
from models.workers_parents import WorkersParents


def handle_get_workers_parents(id: int):
    with Session(engine) as session:
        worker_parents = session.exec(
            select(WorkersParents).where(WorkersParents.worker_id == id)
        ).all()

        return worker_parents


def handle_post_workers_parents(worker_parent: WorkersParents):
    with Session(engine) as session:
        session.add(worker_parent)

        session.commit()

        session.refresh(worker_parent)

        return worker_parent


def handle_delete_workers_parents(id: int):
    with Session(engine) as session:
        get_worker_parent = select(WorkersParents).where(WorkersParents.id == id)

        worker_parent = session.exec(get_worker_parent).first()

        session.delete(worker_parent)

        session.commit()

        return {"success": True}
