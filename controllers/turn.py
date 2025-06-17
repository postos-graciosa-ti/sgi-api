from datetime import datetime

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select

from database.sqlite import engine
from functions.auth import AuthUser
from functions.logs import log_action
from models.turn import Turn
from pyhints.turns import PutTurn


def handle_get_subsidiarie_turns(id: int):
    with Session(engine) as session:
        query = select(Turn).where(Turn.subsidiarie_id == id)

        turns = session.exec(query).all()

        return turns


def handle_get_turns():
    with Session(engine) as session:
        turns = session.exec(select(Turn)).all()

        return turns


def handle_get_turn_by_id(id: int):
    with Session(engine) as session:
        turn = session.exec(select(Turn).where(Turn.id == id)).one()

        return turn


def handle_post_turns(request: Request, formData: Turn, user: AuthUser):
    formData.start_time = datetime.strptime(formData.start_time, "%H:%M").time()

    formData.start_interval_time = datetime.strptime(
        formData.start_interval_time, "%H:%M"
    ).time()

    formData.end_time = datetime.strptime(formData.end_time, "%H:%M").time()

    formData.end_interval_time = datetime.strptime(
        formData.end_interval_time, "%H:%M"
    ).time()

    with Session(engine) as session:
        session.add(formData)

        session.commit()

        session.refresh(formData)

        log_action(
            action="post",
            table_name="turns",
            record_id=formData.id,
            user_id=user["id"],
            details={
                "before": None,
                "after": jsonable_encoder(formData),
            },
            endpoint=str(request.url.path),
        )

        return formData


def handle_put_turn(request: Request, id: int, formData: PutTurn, user: AuthUser):
    formData.start_time = datetime.strptime(formData.start_time, "%H:%M").time()

    formData.start_interval_time = datetime.strptime(
        formData.start_interval_time, "%H:%M"
    ).time()

    formData.end_time = datetime.strptime(formData.end_time, "%H:%M").time()

    formData.end_interval_time = datetime.strptime(
        formData.end_interval_time, "%H:%M"
    ).time()

    with Session(engine) as session:
        statement = select(Turn).where(Turn.id == id)

        turn = session.exec(statement).first()

        before_data = turn.dict()

        turn.name = formData.name

        turn.start_time = formData.start_time

        turn.start_interval_time = formData.start_interval_time

        turn.end_time = formData.end_time

        turn.end_interval_time = formData.end_interval_time

        turn.week = formData.week

        session.commit()

        session.refresh(turn)

        log_action(
            action="put",
            table_name="turns",
            record_id=id,
            user_id=user["id"],
            details={
                "before": jsonable_encoder(before_data),
                "after": jsonable_encoder(turn),
            },
            endpoint=str(request.url.path),
        )

        return turn


def handle_delete_turn(request: Request, id: int, user: AuthUser):
    with Session(engine) as session:
        turn = session.get(Turn, id)

        before_data = turn.dict()

        session.delete(turn)

        session.commit()

        log_action(
            action="put",
            table_name="turns",
            record_id=turn.id,
            user_id=user["id"],
            details={
                "before": jsonable_encoder(before_data),
                "after": "",
            },
            endpoint=str(request.url.path),
        )

        return {"status": "ok"}
