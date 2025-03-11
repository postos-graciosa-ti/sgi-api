from sqlmodel import Session, select

from database.sqlite import engine
from models.month import Month


def seed_months():
    with Session(engine) as session:
        existing_months = session.exec(select(Month)).all()

        if not existing_months:
            months = [
                Month(id=1, name="janeiro"),
                Month(id=2, name="fevereiro"),
                Month(id=3, name="março"),
                Month(id=4, name="abril"),
                Month(id=5, name="maio"),
                Month(id=6, name="junho"),
                Month(id=7, name="julho"),
                Month(id=8, name="agosto"),
                Month(id=9, name="setembro"),
                Month(id=10, name="outubro"),
                Month(id=11, name="novembro"),
                Month(id=12, name="dezembro"),
            ]

            session.add_all(months)

            session.commit()
