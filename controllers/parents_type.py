from sqlmodel import Session, select

from database.sqlite import engine
from models.parents_type import ParentsType


def handle_get_parents_type():
    with Session(engine) as session:
        parents_types = session.exec(select(ParentsType)).all()

        return parents_types
