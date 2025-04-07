from sqlmodel import Session, select

from database.sqlite import engine
from models.nationalities import Nationalities


def seed_nationalities():
    with Session(engine) as session:
        exist_nationalitie = session.exec(select(Nationalities)).first()

        if not exist_nationalitie:
            nationalities = [
                Nationalities(name="Brasileiro"),
                Nationalities(name="Venezuelano"),
            ]

            session.add_all(nationalities)

            session.commit()
