from repository.functions import create, find_all
from models.scale import Scale
from sqlmodel import Session, select
from database.sqlite import engine

def create_or_update_scale(scale: Scale):
    with Session(engine) as session:
        statement = select(Scale).where(Scale.id == scale.id)

        db_scale = session.exec(statement).first()

        if db_scale:
            return update_scale(scale.id, scale)
        else:
            return create(scale)


def update_scale(id: int, scale: Scale):
    with Session(engine) as session:
        statement = select(Scale).where(Scale.id == id)

        db_scale = session.exec(statement).first()

        db_scale.date = scale.date

        db_scale.worker_id = scale.worker_id

        db_scale.month_id = scale.month_id

        session.commit()

        session.refresh(db_scale)

        return db_scale
