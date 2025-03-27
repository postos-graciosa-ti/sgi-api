from sqlmodel import Session

from database.sqlite import engine
from models.civil_status import CivilStatus


def seed_civil_status():
    civil_statuses = [
        CivilStatus(name="Solteiro(a)"),
        CivilStatus(name="Casado(a)"),
        CivilStatus(name="Divorciado(a)"),
        CivilStatus(name="Viúvo(a)"),
        CivilStatus(name="União estável"),
        CivilStatus(name="Separado(a)"),
    ]

    with Session(engine) as session:
        session.add_all(civil_statuses)

        session.commit()
