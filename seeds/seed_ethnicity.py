from sqlmodel import select
from sqlmodel import Session
from database.sqlite import engine
from models.ethnicity import Ethnicity


def seed_ethnicities():
    with Session(engine) as session:
        ethnicities = [
            Ethnicity(name="Branco"),
            Ethnicity(name="Preto"),
            Ethnicity(name="Pardo"),
            Ethnicity(name="Indígena"),
            Ethnicity(name="Asiático"),
            Ethnicity(name="Outro"),
        ]

        session.add_all(ethnicities)

        session.commit()
