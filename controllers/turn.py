from datetime import datetime

from sqlmodel import Session, select

from database.sqlite import engine
from models.turn import Turn
from pyhints.turns import PutTurn
from repository.functions import create, delete, find_all, update


def handle_get_turns():
    turns = find_all(Turn)

    return turns


def handle_post_turns(formData: Turn):
    formData.start_time = datetime.strptime(formData.start_time, "%H:%M").time()

    formData.start_interval_time = datetime.strptime(
        formData.start_interval_time, "%H:%M"
    ).time()

    formData.end_time = datetime.strptime(formData.end_time, "%H:%M").time()

    formData.end_interval_time = datetime.strptime(
        formData.end_interval_time, "%H:%M"
    ).time()

    turns = create(formData)

    return turns


def handle_put_turn(id: int, formData: PutTurn):
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

        turn.name = formData.name

        turn.start_time = formData.start_time

        turn.start_interval_time = formData.start_interval_time

        turn.end_time = formData.end_time

        turn.end_interval_time = formData.end_interval_time

        session.commit()

        session.refresh(turn)
    return turn


def handle_delete_turn(id: int):
    return delete(id, Turn)
