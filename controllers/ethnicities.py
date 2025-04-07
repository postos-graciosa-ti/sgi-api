from sqlmodel import Session, select

from database.sqlite import engine
from models.ethnicity import Ethnicity


def handle_get_ethnicities():
    with Session(engine) as session:
        ethnicities = session.exec(select(Ethnicity)).all()

        return ethnicities
