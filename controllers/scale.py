from repository.functions import create, find_all
from models.scale import Scale
from sqlmodel import Session, select
from database.sqlite import engine
from repository.scale import update_scale


def handle_get_scale():
    scales = find_all(Scale)

    return scales


def handle_post_scale(scale: Scale):
    scale = create(scale)

    return scale


def handle_get_scale_by_worker_and_month(worker_id: int, month_id: int):
    with Session(engine) as session:
        statement = select(Scale).where(
            Scale.worker_id == worker_id, Scale.month_id == month_id
        )

        scale = session.exec(statement).first()
    return scale


def handle_put_scale(id: int, scale: Scale):
    scale = update_scale(id, scale)

    return scale
