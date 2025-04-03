from sqlmodel import Session, select

from database.sqlite import engine
from models.genders import Genders


def handle_get_genders():
    with Session(engine) as session:
        genders = session.exec(select(Genders)).all()

        return genders
