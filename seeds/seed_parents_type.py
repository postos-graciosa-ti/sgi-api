from sqlmodel import Session, select
from database.sqlite import engine
from models.parents_type import ParentsType


def seed_parents_type():
    parents_types = [
        ParentsType(name="Banco do Brasil"),
        ParentsType(name="Cônjugue"),
        ParentsType(name="Filho(a)"),
    ]

    with Session(engine) as session:
        has_parents_types = session.exec(select(ParentsType)).first()

        if not has_parents_types:
            session.add_all(parents_types)

            session.commit()
