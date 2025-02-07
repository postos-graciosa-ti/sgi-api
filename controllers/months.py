from sqlmodel import Session, select

from database.sqlite import engine
from models.month import Month


def handle_get_months():
    with Session(engine) as session:
        months = session.exec(select(Month)).all()

        return months
